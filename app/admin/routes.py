from flask import render_template, redirect, url_for, flash, request, abort
from flask_login import login_required, current_user
from functools import wraps
from app import db
from app.admin import bp
from app.models import User, Assessment, Payment, Response, Report
from sqlalchemy import func
from datetime import datetime, timedelta

def admin_required(f):
    """Decorator to require admin access"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or current_user.email != 'vicgupta@gmail.com':
            abort(403)  # Forbidden
        return f(*args, **kwargs)
    return decorated_function

@bp.route('/admin')
@login_required
@admin_required
def index():
    """Admin dashboard with overview statistics"""
    # Get basic statistics
    total_users = User.query.count()
    total_assessments = Assessment.query.count()
    completed_assessments = Assessment.query.filter_by(completed=True).count()
    total_payments = Payment.query.count()
    successful_payments = Payment.query.filter_by(status='succeeded').count()

    # Get recent activity
    recent_users = User.query.order_by(User.created_at.desc()).limit(5).all()
    recent_payments = Payment.query.order_by(Payment.created_at.desc()).limit(5).all()
    recent_assessments = Assessment.query.order_by(Assessment.created_at.desc()).limit(5).all()

    # Revenue statistics
    total_revenue = db.session.query(func.sum(Payment.amount)).filter_by(status='succeeded').scalar() or 0
    total_revenue_dollars = total_revenue / 100  # Convert from cents to dollars

    # Assessment type breakdown
    simple_assessments = Assessment.query.filter_by(type='simple').count()
    premium_assessments = Assessment.query.filter_by(type='premium').count()

    return render_template('admin/dashboard.html',
                         total_users=total_users,
                         total_assessments=total_assessments,
                         completed_assessments=completed_assessments,
                         total_payments=total_payments,
                         successful_payments=successful_payments,
                         recent_users=recent_users,
                         recent_payments=recent_payments,
                         recent_assessments=recent_assessments,
                         total_revenue=total_revenue_dollars,
                         simple_assessments=simple_assessments,
                         premium_assessments=premium_assessments)

@bp.route('/admin/users')
@login_required
@admin_required
def users():
    """View all users"""
    page = request.args.get('page', 1, type=int)
    users = User.query.order_by(User.created_at.desc()).paginate(
        page=page, per_page=20, error_out=False)
    return render_template('admin/users.html', users=users)

@bp.route('/admin/user/<int:user_id>')
@login_required
@admin_required
def user_detail(user_id):
    """View detailed information about a specific user"""
    user = User.query.get_or_404(user_id)
    assessments = Assessment.query.filter_by(user_id=user_id).order_by(Assessment.created_at.desc()).all()
    payments = Payment.query.filter_by(user_id=user_id).order_by(Payment.created_at.desc()).all()
    return render_template('admin/user_detail.html', user=user, assessments=assessments, payments=payments)

@bp.route('/admin/payments')
@login_required
@admin_required
def payments():
    """View all payments"""
    page = request.args.get('page', 1, type=int)
    status_filter = request.args.get('status', '')

    query = Payment.query
    if status_filter:
        query = query.filter_by(status=status_filter)

    payments = query.order_by(Payment.created_at.desc()).paginate(
        page=page, per_page=20, error_out=False)

    # Get unique statuses for filter dropdown
    statuses = db.session.query(Payment.status).distinct().all()
    statuses = [status[0] for status in statuses]

    return render_template('admin/payments.html', payments=payments, statuses=statuses, current_status=status_filter)

@bp.route('/admin/assessments')
@login_required
@admin_required
def assessments():
    """View all assessments"""
    page = request.args.get('page', 1, type=int)
    type_filter = request.args.get('type', '')
    status_filter = request.args.get('status', '')

    query = Assessment.query
    if type_filter:
        query = query.filter_by(type=type_filter)
    if status_filter == 'completed':
        query = query.filter_by(completed=True)
    elif status_filter == 'in_progress':
        query = query.filter_by(completed=False)

    assessments = query.order_by(Assessment.created_at.desc()).paginate(
        page=page, per_page=20, error_out=False)

    return render_template('admin/assessments.html',
                         assessments=assessments,
                         current_type=type_filter,
                         current_status=status_filter)

@bp.route('/admin/assessment/<int:assessment_id>')
@login_required
@admin_required
def assessment_detail(assessment_id):
    """View detailed information about a specific assessment"""
    assessment = Assessment.query.get_or_404(assessment_id)
    responses = Response.query.filter_by(assessment_id=assessment_id).order_by(Response.question_id).all()
    reports = Report.query.filter_by(assessment_id=assessment_id).order_by(Report.generated_at.desc()).all()
    return render_template('admin/assessment_detail.html',
                         assessment=assessment,
                         responses=responses,
                         reports=reports)

@bp.route('/admin/reports')
@login_required
@admin_required
def reports():
    """View all reports"""
    page = request.args.get('page', 1, type=int)
    reports = Report.query.order_by(Report.generated_at.desc()).paginate(
        page=page, per_page=20, error_out=False)
    return render_template('admin/reports.html', reports=reports)

@bp.route('/admin/analytics')
@login_required
@admin_required
def analytics():
    """View analytics and insights"""
    # Get data for the last 30 days
    thirty_days_ago = datetime.utcnow() - timedelta(days=30)

    # User registration over time
    daily_users = db.session.query(
        func.date(User.created_at).label('date'),
        func.count(User.id).label('count')
    ).filter(User.created_at >= thirty_days_ago).group_by(
        func.date(User.created_at)
    ).order_by('date').all()

    # Assessment completion over time
    daily_assessments = db.session.query(
        func.date(Assessment.completed_at).label('date'),
        func.count(Assessment.id).label('count')
    ).filter(
        Assessment.completed_at >= thirty_days_ago,
        Assessment.completed == True
    ).group_by(
        func.date(Assessment.completed_at)
    ).order_by('date').all()

    # Payment success over time
    daily_payments = db.session.query(
        func.date(Payment.created_at).label('date'),
        func.count(Payment.id).label('count'),
        func.sum(Payment.amount).label('revenue')
    ).filter(
        Payment.created_at >= thirty_days_ago,
        Payment.status == 'succeeded'
    ).group_by(
        func.date(Payment.created_at)
    ).order_by('date').all()

    return render_template('admin/analytics.html',
                         daily_users=daily_users,
                         daily_assessments=daily_assessments,
                         daily_payments=daily_payments)