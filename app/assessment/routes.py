from flask import render_template, redirect, url_for, flash, request, session
from flask_login import login_required, current_user
from datetime import datetime
from app import db
from app.assessment import bp
from app.models import Assessment, Response, Report, Payment
from app.assessment.scoring import calculate_spike_factor, generate_personality_insights
from app.assessment.premium_questions import PREMIUM_ASSESSMENT_QUESTIONS

# Sample assessment questions
ASSESSMENT_QUESTIONS = [
    {
        'id': 1,
        'question': 'I enjoy taking on challenging projects even when the outcome is uncertain.',
        'type': 'likert'
    },
    {
        'id': 2,
        'question': 'I often volunteer for leadership roles in group settings.',
        'type': 'likert'
    },
    {
        'id': 3,
        'question': 'I bounce back quickly from setbacks and failures.',
        'type': 'likert'
    },
    {
        'id': 4,
        'question': 'I prefer to work on multiple projects simultaneously rather than one at a time.',
        'type': 'likert'
    },
    {
        'id': 5,
        'question': 'I actively seek feedback to improve my performance.',
        'type': 'likert'
    },
    {
        'id': 6,
        'question': 'I feel energized by competitive environments.',
        'type': 'likert'
    },
    {
        'id': 7,
        'question': 'I am comfortable making decisions with incomplete information.',
        'type': 'likert'
    },
    {
        'id': 8,
        'question': 'I enjoy networking and meeting new people in professional settings.',
        'type': 'likert'
    },
    {
        'id': 9,
        'question': 'I often initiate new ideas and innovations in my work.',
        'type': 'likert'
    },
    {
        'id': 10,
        'question': 'I maintain high performance even under tight deadlines.',
        'type': 'likert'
    }
]

@bp.route('/simple')
@login_required
def simple():
    # Check if user has already completed an assessment
    completed_assessment = Assessment.query.filter_by(
        user_id=current_user.id,
        completed=True
    ).first()

    if completed_assessment:
        flash('You have already completed the assessment. You can view your report below.')
        report = completed_assessment.reports.first()
        if report:
            return redirect(url_for('reports.view', report_id=report.id))
        else:
            return redirect(url_for('dashboard.index'))

    # Check if user has any incomplete assessments
    incomplete_assessment = Assessment.query.filter_by(
        user_id=current_user.id,
        completed=False
    ).first()

    if incomplete_assessment:
        # Continue existing assessment
        current_question = len(incomplete_assessment.responses.all()) + 1
        if current_question > len(ASSESSMENT_QUESTIONS):
            # All questions answered, complete assessment
            return redirect(url_for('assessment.complete', assessment_id=incomplete_assessment.id))
        else:
            return redirect(url_for('assessment.question', question_id=current_question))

    # Start new assessment (user has no assessments yet)
    assessment = Assessment(user_id=current_user.id, type='simple')
    db.session.add(assessment)
    db.session.commit()
    current_question = 1

    return redirect(url_for('assessment.question', question_id=current_question))


@bp.route('/question/<int:question_id>', methods=['GET', 'POST'])
@login_required
def question(question_id):
    if question_id < 1 or question_id > len(ASSESSMENT_QUESTIONS):
        flash('Invalid question number')
        return redirect(url_for('assessment.simple'))

    # Get current assessment
    assessment = Assessment.query.filter_by(
        user_id=current_user.id,
        completed=False
    ).first()

    if not assessment:
        return redirect(url_for('assessment.simple'))

    question_data = ASSESSMENT_QUESTIONS[question_id - 1]

    if request.method == 'POST':
        answer = request.form.get('answer')
        if not answer:
            flash('Please select an answer')
            return render_template('assessment/question.html',
                                 question=question_data,
                                 question_num=question_id,
                                 total_questions=len(ASSESSMENT_QUESTIONS))

        # Save response
        response = Response(
            assessment_id=assessment.id,
            question_id=question_id,
            answer=answer
        )
        db.session.add(response)
        db.session.commit()

        # Check if this was the last question
        if question_id >= len(ASSESSMENT_QUESTIONS):
            return redirect(url_for('assessment.complete', assessment_id=assessment.id))
        else:
            return redirect(url_for('assessment.question', question_id=question_id + 1))

    return render_template('assessment/question.html',
                         question=question_data,
                         question_num=question_id,
                         total_questions=len(ASSESSMENT_QUESTIONS))

@bp.route('/complete/<int:assessment_id>')
@login_required
def complete(assessment_id):
    assessment = Assessment.query.get_or_404(assessment_id)

    if assessment.user_id != current_user.id:
        flash('Access denied')
        return redirect(url_for('dashboard.index'))

    if assessment.completed:
        # Already completed, redirect to report
        report = assessment.reports.first()
        if report:
            return redirect(url_for('reports.view', report_id=report.id))

    # Mark assessment as completed
    assessment.completed = True
    assessment.completed_at = datetime.utcnow()

    # Generate report
    responses = assessment.responses.all()
    spike_factor = calculate_spike_factor(responses)
    insights = generate_personality_insights(spike_factor, responses)

    # Create report content
    report_content = f"""
    <h2>Your Spike Factor Assessment Results</h2>
    <div class="alert alert-info">
        <h3>Spike Factor Score: {insights['spike_factor']}%</h3>
        <h4>Category: {insights['category']}</h4>
    </div>

    <h3>Your Strengths:</h3>
    <ul>
    {''.join([f'<li>{strength}</li>' for strength in insights['strengths']])}
    </ul>

    <h3>Areas for Growth:</h3>
    <ul>
    {''.join([f'<li>{area}</li>' for area in insights['growth_areas']])}
    </ul>

    <h3>Recommendations:</h3>
    <ul>
    {''.join([f'<li>{rec}</li>' for rec in insights['recommendations']])}
    </ul>
    """

    report = Report(
        assessment_id=assessment.id,
        content=report_content
    )

    db.session.add(report)
    db.session.commit()

    return redirect(url_for('reports.view', report_id=report.id))

@bp.route('/premium')
@login_required
def premium():
    """Start or continue premium assessment"""
    # Check if user has paid for premium assessment
    if not current_user.has_premium_access():
        flash('You need to purchase the premium assessment first.')
        return redirect(url_for('payment.checkout_premium'))

    # Get any successful payment for linking to assessment
    payment = Payment.query.filter_by(
        user_id=current_user.id,
        assessment_type='premium',
        status='succeeded'
    ).first()

    # Check if user has already completed premium assessment
    completed_assessment = Assessment.query.filter_by(
        user_id=current_user.id,
        type='premium',
        completed=True,
        payment_id=payment.id
    ).first()

    if completed_assessment:
        flash('You have already completed the premium assessment. You can view your report below.')
        report = completed_assessment.reports.first()
        if report:
            return redirect(url_for('reports.view', report_id=report.id))
        else:
            return redirect(url_for('dashboard.index'))

    # Check if user has any incomplete premium assessments
    incomplete_assessment = Assessment.query.filter_by(
        user_id=current_user.id,
        type='premium',
        completed=False,
        payment_id=payment.id
    ).first()

    if incomplete_assessment:
        # Continue existing assessment
        current_question = len(incomplete_assessment.responses.all()) + 1
        if current_question > len(PREMIUM_ASSESSMENT_QUESTIONS):
            # All questions answered, complete assessment
            return redirect(url_for('assessment.premium_complete', assessment_id=incomplete_assessment.id))
        else:
            return redirect(url_for('assessment.premium_question', question_id=current_question))

    # Start new premium assessment
    assessment = Assessment(
        user_id=current_user.id,
        type='premium',
        payment_id=payment.id
    )
    db.session.add(assessment)
    db.session.commit()

    return redirect(url_for('assessment.premium_question', question_id=1))

@bp.route('/premium/question/<int:question_id>', methods=['GET', 'POST'])
@login_required
def premium_question(question_id):
    """Handle premium assessment questions"""
    if question_id < 1 or question_id > len(PREMIUM_ASSESSMENT_QUESTIONS):
        flash('Invalid question number')
        return redirect(url_for('assessment.premium'))

    # Verify user has access to premium assessment
    if not current_user.has_premium_access():
        flash('You need to purchase the premium assessment first.')
        return redirect(url_for('payment.checkout_premium'))

    # Get any successful payment for linking to assessment
    payment = Payment.query.filter_by(
        user_id=current_user.id,
        assessment_type='premium',
        status='succeeded'
    ).first()

    # Get current assessment
    assessment = Assessment.query.filter_by(
        user_id=current_user.id,
        type='premium',
        completed=False,
        payment_id=payment.id
    ).first()

    if not assessment:
        return redirect(url_for('assessment.premium'))

    question_data = PREMIUM_ASSESSMENT_QUESTIONS[question_id - 1]

    if request.method == 'POST':
        answer = request.form.get('answer')
        if not answer:
            flash('Please select an answer')
            return render_template('assessment/premium_question.html',
                                 question=question_data,
                                 question_num=question_id,
                                 total_questions=len(PREMIUM_ASSESSMENT_QUESTIONS))

        # Check if response already exists for this question (premium user might be revisiting)
        existing_response = Response.query.filter_by(
            assessment_id=assessment.id,
            question_id=question_id
        ).first()

        if existing_response:
            # Update existing response for premium users (allow response modification)
            existing_response.answer = answer
            existing_response.created_at = datetime.utcnow()
        else:
            # Save new response
            response = Response(
                assessment_id=assessment.id,
                question_id=question_id,
                answer=answer
            )
            db.session.add(response)

        db.session.commit()

        # Check if this was the last question
        if question_id >= len(PREMIUM_ASSESSMENT_QUESTIONS):
            return redirect(url_for('assessment.premium_complete', assessment_id=assessment.id))
        else:
            return redirect(url_for('assessment.premium_question', question_id=question_id + 1))

    return render_template('assessment/premium_question.html',
                         question=question_data,
                         question_num=question_id,
                         total_questions=len(PREMIUM_ASSESSMENT_QUESTIONS))

@bp.route('/premium/complete/<int:assessment_id>')
@login_required
def premium_complete(assessment_id):
    """Complete premium assessment and generate comprehensive report"""
    assessment = Assessment.query.get_or_404(assessment_id)

    if assessment.user_id != current_user.id or assessment.type != 'premium':
        flash('Access denied')
        return redirect(url_for('dashboard.index'))

    if assessment.completed:
        # Already completed, redirect to report
        report = assessment.reports.first()
        if report:
            return redirect(url_for('reports.view', report_id=report.id))

    # Mark assessment as completed
    assessment.completed = True
    assessment.completed_at = datetime.utcnow()

    # Generate comprehensive report
    responses = assessment.responses.all()
    from app.assessment.premium_scoring import generate_comprehensive_report
    report_content = generate_comprehensive_report(responses)

    report = Report(
        assessment_id=assessment.id,
        content=report_content
    )

    db.session.add(report)
    db.session.commit()

    return redirect(url_for('reports.view', report_id=report.id))