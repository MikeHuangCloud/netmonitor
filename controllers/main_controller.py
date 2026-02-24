from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required
from models import db, Target
from services import PingService

main_bp = Blueprint('main', __name__)


@main_bp.route('/')
@login_required
def dashboard():
    """儀表板首頁"""
    stats = PingService.get_dashboard_stats()
    targets = Target.query.all()
    return render_template('dashboard.html', stats=stats, targets=targets)


@main_bp.route('/targets')
@login_required
def targets():
    """目標管理頁面"""
    targets = Target.query.all()
    return render_template('targets.html', targets=targets)


@main_bp.route('/targets/add', methods=['POST'])
@login_required
def add_target():
    """新增監控目標"""
    name = request.form.get('name')
    ip_address = request.form.get('ip_address')
    
    if not name or not ip_address:
        flash('名稱和 IP 位址為必填', 'error')
        return redirect(url_for('main.targets'))
    
    target = Target(name=name, ip_address=ip_address, is_active=True)
    db.session.add(target)
    db.session.commit()
    
    flash(f'已新增監控目標: {name}', 'success')
    return redirect(url_for('main.targets'))


@main_bp.route('/targets/<int:id>/edit', methods=['POST'])
@login_required
def edit_target(id):
    """編輯監控目標"""
    target = Target.query.get_or_404(id)
    
    target.name = request.form.get('name', target.name)
    target.ip_address = request.form.get('ip_address', target.ip_address)
    target.is_active = request.form.get('is_active') == 'on'
    
    db.session.commit()
    flash(f'已更新監控目標: {target.name}', 'success')
    return redirect(url_for('main.targets'))


@main_bp.route('/targets/<int:id>/delete', methods=['POST'])
@login_required
def delete_target(id):
    """刪除監控目標"""
    target = Target.query.get_or_404(id)
    name = target.name
    
    db.session.delete(target)
    db.session.commit()
    
    flash(f'已刪除監控目標: {name}', 'success')
    return redirect(url_for('main.targets'))


@main_bp.route('/targets/<int:id>/toggle', methods=['POST'])
@login_required
def toggle_target(id):
    """切換目標啟用狀態"""
    target = Target.query.get_or_404(id)
    target.is_active = not target.is_active
    db.session.commit()
    
    status = '啟用' if target.is_active else '停用'
    flash(f'{target.name} 已{status}', 'success')
    return redirect(url_for('main.targets'))


@main_bp.route('/detail/<int:id>')
@login_required
def detail(id):
    """目標詳細頁面"""
    target = Target.query.get_or_404(id)
    return render_template('detail.html', target=target)
