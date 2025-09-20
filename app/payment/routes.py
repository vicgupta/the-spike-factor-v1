import stripe
from flask import render_template, redirect, url_for, flash, request, jsonify, current_app
from flask_login import login_required, current_user
from datetime import datetime
from app import db
from app.payment import bp
from app.models import Payment, Assessment

@bp.route('/checkout/premium')
@login_required
def checkout_premium():
    """Display checkout page for premium assessment"""
    # Check if user already has a pending or completed premium assessment
    existing_payment = Payment.query.filter_by(
        user_id=current_user.id,
        assessment_type='premium'
    ).filter(Payment.status.in_(['succeeded', 'pending'])).first()

    if existing_payment:
        if existing_payment.status == 'succeeded':
            # User already paid, redirect to assessment
            assessment = Assessment.query.filter_by(
                user_id=current_user.id,
                type='premium',
                payment_id=existing_payment.id
            ).first()
            if assessment and not assessment.completed:
                return redirect(url_for('assessment.premium_question', question_id=1))
            elif assessment and assessment.completed:
                flash('You have already completed the premium assessment.')
                return redirect(url_for('dashboard.index'))
        elif existing_payment.status == 'pending':
            flash('You have a pending payment. Please complete it or contact support.')
            return redirect(url_for('dashboard.index'))

    return render_template('payment/checkout.html',
                         amount=1000,  # $10.00 in cents
                         stripe_public_key=current_app.config['STRIPE_PUBLISHABLE_KEY'])

@bp.route('/create-payment-intent', methods=['POST'])
@login_required
def create_payment_intent():
    """Create a Stripe payment intent for premium assessment"""
    try:
        stripe.api_key = current_app.config['STRIPE_SECRET_KEY']

        # Create payment intent
        intent = stripe.PaymentIntent.create(
            amount=1000,  # $10.00 in cents
            currency='usd',
            metadata={
                'user_id': current_user.id,
                'assessment_type': 'premium'
            }
        )

        # Store payment in database
        payment = Payment(
            user_id=current_user.id,
            stripe_payment_intent_id=intent.id,
            amount=1000,
            currency='usd',
            status='pending',
            assessment_type='premium'
        )
        db.session.add(payment)
        db.session.commit()

        return jsonify({
            'client_secret': intent.client_secret,
            'payment_id': payment.id
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 400

@bp.route('/payment-success')
@login_required
def payment_success():
    """Handle successful payment and create assessment"""
    payment_intent_id = request.args.get('payment_intent')

    if not payment_intent_id:
        flash('Invalid payment confirmation.')
        return redirect(url_for('dashboard.index'))

    # Find the payment record
    payment = Payment.query.filter_by(
        stripe_payment_intent_id=payment_intent_id,
        user_id=current_user.id
    ).first()

    if not payment:
        flash('Payment record not found.')
        return redirect(url_for('dashboard.index'))

    # Verify payment with Stripe
    try:
        stripe.api_key = current_app.config['STRIPE_SECRET_KEY']
        intent = stripe.PaymentIntent.retrieve(payment_intent_id)

        if intent.status == 'succeeded':
            # Update payment status
            payment.status = 'succeeded'
            payment.updated_at = datetime.utcnow()

            # Create premium assessment
            assessment = Assessment(
                user_id=current_user.id,
                type='premium',
                payment_id=payment.id
            )
            db.session.add(assessment)
            db.session.commit()

            flash('Payment successful! You can now take the comprehensive assessment.')
            return redirect(url_for('assessment.premium'))
        else:
            flash('Payment was not successful. Please try again.')
            return redirect(url_for('payment.checkout_premium'))

    except Exception as e:
        flash('Error verifying payment. Please contact support.')
        return redirect(url_for('dashboard.index'))

@bp.route('/webhook', methods=['POST'])
def stripe_webhook():
    """Handle Stripe webhooks"""
    payload = request.get_data()
    sig_header = request.headers.get('Stripe-Signature')

    try:
        stripe.api_key = current_app.config['STRIPE_SECRET_KEY']
        endpoint_secret = current_app.config['STRIPE_WEBHOOK_SECRET']

        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )

        if event['type'] == 'payment_intent.succeeded':
            payment_intent = event['data']['object']

            # Update payment status in database
            payment = Payment.query.filter_by(
                stripe_payment_intent_id=payment_intent['id']
            ).first()

            if payment:
                payment.status = 'succeeded'
                payment.updated_at = datetime.utcnow()
                db.session.commit()

        elif event['type'] == 'payment_intent.payment_failed':
            payment_intent = event['data']['object']

            # Update payment status in database
            payment = Payment.query.filter_by(
                stripe_payment_intent_id=payment_intent['id']
            ).first()

            if payment:
                payment.status = 'failed'
                payment.updated_at = datetime.utcnow()
                db.session.commit()

        return jsonify({'status': 'success'})

    except ValueError as e:
        return jsonify({'error': 'Invalid payload'}), 400
    except stripe.error.SignatureVerificationError as e:
        return jsonify({'error': 'Invalid signature'}), 400