from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
from config import Config


scheduler = BackgroundScheduler()


def init_scheduler(app):
    """初始化排程器"""
    from services import PingService
    
    def ping_job():
        """執行 ping 作業"""
        with app.app_context():
            try:
                results = PingService.execute_all_pings()
                print(f"[Scheduler] Ping completed for {len(results)} targets")
            except Exception as e:
                print(f"[Scheduler] Ping error: {e}")
    
    # 新增定時任務
    scheduler.add_job(
        func=ping_job,
        trigger=IntervalTrigger(seconds=Config.PING_INTERVAL_SECONDS),
        id='ping_job',
        name='Execute ping for all targets',
        replace_existing=True
    )
    
    scheduler.start()
    print(f"[Scheduler] Started with interval: {Config.PING_INTERVAL_SECONDS} seconds")


def shutdown_scheduler():
    """關閉排程器"""
    if scheduler.running:
        scheduler.shutdown()
        print("[Scheduler] Shutdown completed")
