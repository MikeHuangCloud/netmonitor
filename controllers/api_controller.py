from flask import Blueprint, jsonify, request
from flask_login import login_required
from services import PingService
from models import Target

api_bp = Blueprint('api', __name__, url_prefix='/api')


@api_bp.route('/stats')
@login_required
def get_stats():
    """取得儀表板統計數據"""
    stats = PingService.get_dashboard_stats()
    return jsonify(stats)


@api_bp.route('/chart-data')
@login_required
def get_chart_data():
    """取得圖表數據"""
    hours = request.args.get('hours', 24, type=int)
    data = PingService.get_chart_data(hours)
    return jsonify(data)


@api_bp.route('/targets/<int:id>/history')
@login_required
def get_target_history(id):
    """取得目標歷史數據"""
    hours = request.args.get('hours', 24, type=int)
    history = PingService.get_target_history(id, hours)
    return jsonify(history)


@api_bp.route('/ping/execute', methods=['POST'])
@login_required
def execute_ping():
    """手動執行一次 ping"""
    results = PingService.execute_all_pings()
    return jsonify({
        'status': 'success',
        'results': results
    })


@api_bp.route('/targets/<int:id>/ping', methods=['POST'])
@login_required
def ping_single_target(id):
    """對單一目標執行 ping"""
    target = Target.query.get_or_404(id)
    result = PingService.ping_target(target)
    return jsonify({
        'target': target.to_dict(),
        'result': result
    })
