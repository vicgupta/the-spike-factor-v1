from flask import render_template, flash, redirect, url_for
from flask_login import login_required, current_user
from app.reports import bp
from app.models import Report

@bp.route('/view/<int:report_id>')
@login_required
def view(report_id):
    report = Report.query.get_or_404(report_id)

    # Check if user owns this report
    if report.assessment.user_id != current_user.id:
        flash('Access denied')
        return redirect(url_for('dashboard.index'))

    return render_template('reports/view.html', report=report)