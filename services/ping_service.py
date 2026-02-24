import subprocess
import re
import platform
from datetime import datetime, timedelta, timezone
from sqlalchemy import func
from models import db, Target, PingRecord
from config import Config

# UTC+8 時區
TZ_UTC8 = timezone(timedelta(hours=8))


class PingService:
    """Ping 執行服務"""
    
    @staticmethod
    def ping_target(target):
        """對單一目標執行 ping"""
        try:
            # 根據作業系統選擇 ping 參數
            param = '-n' if platform.system().lower() == 'windows' else '-c'
            timeout_param = '-w' if platform.system().lower() == 'windows' else '-W'
            
            command = [
                'ping',
                param, str(Config.PING_COUNT),
                timeout_param, str(Config.PING_TIMEOUT),
                target.ip_address
            ]
            
            result = subprocess.run(
                command,
                capture_output=True,
                text=True,
                timeout=Config.PING_TIMEOUT * Config.PING_COUNT + 5
            )
            
            return PingService._parse_ping_result(result.stdout, result.returncode == 0)
            
        except subprocess.TimeoutExpired:
            return {
                'is_success': False,
                'error_message': 'Ping timeout'
            }
        except Exception as e:
            return {
                'is_success': False,
                'error_message': str(e)
            }
    
    @staticmethod
    def _parse_ping_result(output, success):
        """解析 ping 輸出結果"""
        result = {
            'is_success': success,
            'ttl': None,
            'bytes': None,
            'delay_ms': None,
            'packet_loss_percent': 100.0,  # 預設為 100% 丟包
            'error_message': None
        }
        
        if not success or not output:
            result['error_message'] = 'Request timeout or host unreachable'
            return result
        
        # 解析 TTL
        ttl_match = re.search(r'ttl[=:](\d+)', output, re.IGNORECASE)
        if ttl_match:
            result['ttl'] = int(ttl_match.group(1))
        
        # 解析 bytes
        bytes_match = re.search(r'(\d+)\s*bytes', output, re.IGNORECASE)
        if bytes_match:
            result['bytes'] = int(bytes_match.group(1))
        
        # 解析 packet loss percentage
        # Linux format: 1 packets transmitted, 1 received, 0% packet loss
        # Windows format: Packets: Sent = 4, Received = 4, Lost = 0 (0% loss)
        loss_match = re.search(r'(\d+(?:\.\d+)?)\s*%\s*(?:packet\s+)?loss', output, re.IGNORECASE)
        if loss_match:
            result['packet_loss_percent'] = float(loss_match.group(1))
        else:
            # 如果成功且有回應，設為 0%
            if success:
                result['packet_loss_percent'] = 0.0
        
        # 解析平均延遲 (Linux: avg, Windows: Average)
        # Linux format: rtt min/avg/max/mdev = 0.035/0.045/0.055/0.010 ms
        avg_match = re.search(r'[=/](\d+\.?\d*)/(\d+\.?\d*)/(\d+\.?\d*)', output)
        if avg_match:
            result['delay_ms'] = float(avg_match.group(2))
        else:
            # Windows format: Average = 10ms
            avg_match = re.search(r'Average\s*=\s*(\d+)', output)
            if avg_match:
                result['delay_ms'] = float(avg_match.group(1))
            else:
                # 嘗試取得單次 time 值
                time_match = re.search(r'time[=<](\d+\.?\d*)\s*ms', output, re.IGNORECASE)
                if time_match:
                    result['delay_ms'] = float(time_match.group(1))
        
        return result
    
    @staticmethod
    def execute_all_pings():
        """執行所有啟用目標的 ping"""
        targets = Target.query.filter_by(is_active=True).all()
        results = []
        
        for target in targets:
            ping_result = PingService.ping_target(target)
            
            # 儲存記錄
            record = PingRecord(
                target_id=target.id,
                ttl=ping_result.get('ttl'),
                bytes=ping_result.get('bytes'),
                delay_ms=ping_result.get('delay_ms'),
                packet_loss_percent=ping_result.get('packet_loss_percent', 100.0),
                is_success=ping_result.get('is_success', False),
                error_message=ping_result.get('error_message')
            )
            db.session.add(record)
            
            results.append({
                'target': target.to_dict(),
                'result': ping_result
            })
        
        db.session.commit()
        return results
    
    @staticmethod
    def get_dashboard_stats():
        """取得儀表板統計資料"""
        total_targets = Target.query.count()
        active_targets = Target.query.filter_by(is_active=True).count()
        
        # 最近一小時內的記錄
        one_hour_ago = datetime.utcnow() - timedelta(hours=1)
        
        # 取得每個目標的最新狀態
        subquery = db.session.query(
            PingRecord.target_id,
            func.max(PingRecord.created_at).label('latest')
        ).group_by(PingRecord.target_id).subquery()
        
        latest_records = db.session.query(PingRecord).join(
            subquery,
            (PingRecord.target_id == subquery.c.target_id) &
            (PingRecord.created_at == subquery.c.latest)
        ).all()
        
        online_count = sum(1 for r in latest_records if r.is_success)
        offline_count = len(latest_records) - online_count
        
        # 計算平均延遲
        avg_delay = db.session.query(func.avg(PingRecord.delay_ms)).filter(
            PingRecord.created_at >= one_hour_ago,
            PingRecord.is_success == True
        ).scalar() or 0
        
        # 計算平均丟包率
        avg_packet_loss = db.session.query(func.avg(PingRecord.packet_loss_percent)).filter(
            PingRecord.created_at >= one_hour_ago
        ).scalar() or 0
        
        # 最近 24 小時成功率
        day_ago = datetime.utcnow() - timedelta(hours=24)
        total_pings = db.session.query(func.count(PingRecord.id)).filter(
            PingRecord.created_at >= day_ago
        ).scalar() or 0
        
        success_pings = db.session.query(func.count(PingRecord.id)).filter(
            PingRecord.created_at >= day_ago,
            PingRecord.is_success == True
        ).scalar() or 0
        
        success_rate = (success_pings / total_pings * 100) if total_pings > 0 else 0
        
        return {
            'total_targets': total_targets,
            'active_targets': active_targets,
            'online_count': online_count,
            'offline_count': offline_count,
            'avg_delay': round(avg_delay, 2),
            'avg_packet_loss': round(avg_packet_loss, 2),
            'success_rate': round(success_rate, 2),
            'latest_records': [r.to_dict() for r in latest_records]
        }
    
    @staticmethod
    def get_target_history(target_id, hours=24):
        """取得目標的歷史記錄"""
        time_ago = datetime.utcnow() - timedelta(hours=hours)
        
        records = PingRecord.query.filter(
            PingRecord.target_id == target_id,
            PingRecord.created_at >= time_ago
        ).order_by(PingRecord.created_at.asc()).all()
        
        return [r.to_dict() for r in records]
    
    @staticmethod
    def get_chart_data(hours=24):
        """取得圖表數據"""
        time_ago = datetime.utcnow() - timedelta(hours=hours)
        
        targets = Target.query.filter_by(is_active=True).all()
        chart_data = {}
        
        for target in targets:
            records = PingRecord.query.filter(
                PingRecord.target_id == target.id,
                PingRecord.created_at >= time_ago
            ).order_by(PingRecord.created_at.asc()).all()
            
            chart_data[target.id] = {
                'name': target.name,
                'ip': target.ip_address,
                'labels': [r.created_at.replace(tzinfo=timezone.utc).astimezone(TZ_UTC8).strftime('%H:%M:%S') for r in records],
                'delays': [r.delay_ms if r.delay_ms else 0 for r in records],
                'success': [1 if r.is_success else 0 for r in records]
            }
        
        return chart_data
