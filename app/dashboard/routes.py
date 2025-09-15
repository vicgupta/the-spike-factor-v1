from flask import render_template
from flask_login import login_required, current_user
from app.dashboard import bp
from app.models import Assessment, Report

@bp.route('/')
@bp.route('/index')
@login_required
def index():
    assessments = current_user.assessments.order_by(Assessment.created_at.desc()).all()
    return render_template('dashboard/index.html', title='Dashboard', assessments=assessments)

@bp.route('/reports')
@login_required
def reports():
    user_assessments = current_user.assessments.all()
    reports = []
    for assessment in user_assessments:
        reports.extend(assessment.reports.all())
    reports.sort(key=lambda x: x.generated_at, reverse=True)
    return render_template('dashboard/reports.html', title='My Reports', reports=reports)