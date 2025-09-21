import stripe
import logging
from flask import render_template, redirect, url_for, flash, request, jsonify, current_app
from flask_login import login_required, current_user
from datetime import datetime
from app import db
from app.payment import bp
from app.models import Payment, Assessment

# Configure logger for Stripe payments
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

@bp.route('/checkout/premium')
@login_required
def checkout_premium():
    """Display checkout page for premium assessment"""
    logger.info(f"User {current_user.id} accessing premium checkout page")

    # Check if user already has a pending or completed premium assessment
    existing_payment = Payment.query.filter_by(
        user_id=current_user.id,
        assessment_type='premium'
    ).filter(Payment.status.in_(['succeeded', 'pending'])).first()

    if existing_payment:
        logger.info(f"Found existing payment for user {current_user.id}: {existing_payment.id} (status: {existing_payment.status})")
        if existing_payment.status == 'succeeded':
            # User already paid, redirect to assessment
            assessment = Assessment.query.filter_by(
                user_id=current_user.id,
                type='premium',
                payment_id=existing_payment.id
            ).first()
            if assessment and not assessment.completed:
                logger.info(f"Redirecting user {current_user.id} to continue premium assessment {assessment.id}")
                return redirect(url_for('assessment.premium_question', question_id=1))
            elif assessment and assessment.completed:
                logger.info(f"User {current_user.id} already completed premium assessment {assessment.id}")
                flash('You have already completed the premium assessment.')
                return redirect(url_for('dashboard.index'))
        elif existing_payment.status == 'pending':
            logger.warning(f"User {current_user.id} has pending payment {existing_payment.id}")
            flash('You have a pending payment. Please complete it or contact support.')
            return redirect(url_for('dashboard.index'))

    logger.info(f"Showing checkout page to user {current_user.id}")
    return render_template('payment/checkout.html',
                         amount=1000,  # $10.00 in cents
                         stripe_public_key=current_app.config['STRIPE_PUBLISHABLE_KEY'])

@bp.route('/create-payment-intent', methods=['POST'])
@login_required
def create_payment_intent():
    """Create a Stripe payment intent for premium assessment"""
    logger.info(f"Creating payment intent for user {current_user.id}")

    try:
        stripe.api_key = current_app.config['STRIPE_SECRET_KEY']
        logger.debug(f"Stripe API key configured for user {current_user.id}")

        # Create payment intent
        logger.debug(f"Creating Stripe PaymentIntent for user {current_user.id}, amount: 1000 cents")
        intent = stripe.PaymentIntent.create(
            amount=1000,  # $10.00 in cents
            currency='usd',
            metadata={
                'user_id': current_user.id,
                'assessment_type': 'premium'
            }
        )
        logger.info(f"Stripe PaymentIntent created successfully: {intent.id} for user {current_user.id}")
        logger.debug(f"PaymentIntent details - ID: {intent.id}, Status: {intent.status}, Amount: {intent.amount}, Currency: {intent.currency}")

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
        logger.info(f"Payment record created in database: ID {payment.id} for user {current_user.id}")

        response_data = {
            'client_secret': intent.client_secret,
            'payment_id': payment.id
        }
        logger.debug(f"Returning client_secret and payment_id {payment.id} to user {current_user.id}")
        return jsonify(response_data)

    except stripe.error.CardError as e:
        logger.error(f"Stripe CardError for user {current_user.id}: {e.error}")
        return jsonify({'error': f'Card error: {e.error.message}'}), 400
    except stripe.error.RateLimitError as e:
        logger.error(f"Stripe RateLimitError for user {current_user.id}: {e}")
        return jsonify({'error': 'Rate limit exceeded, please try again later'}), 429
    except stripe.error.InvalidRequestError as e:
        logger.error(f"Stripe InvalidRequestError for user {current_user.id}: {e}")
        return jsonify({'error': f'Invalid request: {e}'}), 400
    except stripe.error.AuthenticationError as e:
        logger.error(f"Stripe AuthenticationError for user {current_user.id}: {e}")
        return jsonify({'error': 'Authentication error'}), 500
    except stripe.error.APIConnectionError as e:
        logger.error(f"Stripe APIConnectionError for user {current_user.id}: {e}")
        return jsonify({'error': 'Network communication error'}), 500
    except stripe.error.StripeError as e:
        logger.error(f"Generic Stripe error for user {current_user.id}: {e}")
        return jsonify({'error': f'Payment service error: {e}'}), 500
    except Exception as e:
        logger.error(f"Unexpected error creating payment intent for user {current_user.id}: {str(e)}", exc_info=True)
        return jsonify({'error': 'An unexpected error occurred'}), 500

@bp.route('/payment-success')
@login_required
def payment_success():
    """Handle successful payment and create assessment"""
    payment_intent_id = request.args.get('payment_intent')
    logger.info(f"Payment success callback for user {current_user.id}, payment_intent: {payment_intent_id}")

    if not payment_intent_id:
        logger.warning(f"Payment success called without payment_intent_id for user {current_user.id}")
        flash('Invalid payment confirmation.')
        return redirect(url_for('dashboard.index'))

    # Find the payment record
    payment = Payment.query.filter_by(
        stripe_payment_intent_id=payment_intent_id,
        user_id=current_user.id
    ).first()

    if not payment:
        logger.error(f"Payment record not found for user {current_user.id}, payment_intent: {payment_intent_id}")
        flash('Payment record not found.')
        return redirect(url_for('dashboard.index'))

    logger.info(f"Found payment record {payment.id} for user {current_user.id}")

    # Verify payment with Stripe
    try:
        stripe.api_key = current_app.config['STRIPE_SECRET_KEY']
        logger.debug(f"Retrieving PaymentIntent {payment_intent_id} from Stripe for user {current_user.id}")
        intent = stripe.PaymentIntent.retrieve(payment_intent_id)
        logger.info(f"Retrieved PaymentIntent {payment_intent_id} with status: {intent.status}")
        logger.debug(f"PaymentIntent details - Amount: {intent.amount}, Currency: {intent.currency}")

        if intent.status == 'succeeded':
            logger.info(f"Payment succeeded for user {current_user.id}, updating payment {payment.id}")
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
            logger.info(f"Created premium assessment {assessment.id} for user {current_user.id}")

            flash('Payment successful! You can now take the comprehensive assessment.')
            return redirect(url_for('assessment.premium'))
        else:
            logger.warning(f"Payment intent {payment_intent_id} has status '{intent.status}' instead of 'succeeded' for user {current_user.id}")
            flash('Payment was not successful. Please try again.')
            return redirect(url_for('payment.checkout_premium'))

    except stripe.error.InvalidRequestError as e:
        logger.error(f"Stripe InvalidRequestError retrieving payment intent {payment_intent_id} for user {current_user.id}: {e}")
        flash('Error verifying payment. Please contact support.')
        return redirect(url_for('dashboard.index'))
    except stripe.error.AuthenticationError as e:
        logger.error(f"Stripe AuthenticationError retrieving payment intent {payment_intent_id} for user {current_user.id}: {e}")
        flash('Error verifying payment. Please contact support.')
        return redirect(url_for('dashboard.index'))
    except stripe.error.APIConnectionError as e:
        logger.error(f"Stripe APIConnectionError retrieving payment intent {payment_intent_id} for user {current_user.id}: {e}")
        flash('Error verifying payment. Please contact support.')
        return redirect(url_for('dashboard.index'))
    except stripe.error.StripeError as e:
        logger.error(f"Stripe error retrieving payment intent {payment_intent_id} for user {current_user.id}: {e}")
        flash('Error verifying payment. Please contact support.')
        return redirect(url_for('dashboard.index'))
    except Exception as e:
        logger.error(f"Unexpected error verifying payment intent {payment_intent_id} for user {current_user.id}: {str(e)}", exc_info=True)
        flash('Error verifying payment. Please contact support.')
        return redirect(url_for('dashboard.index'))

@bp.route('/webhook', methods=['POST'])
def stripe_webhook():
    """Handle Stripe webhooks"""
    payload = request.get_data()
    sig_header = request.headers.get('Stripe-Signature')

    logger.info(f"Received Stripe webhook, signature: {sig_header[:20]}..." if sig_header else "No signature")
    logger.debug(f"Webhook payload size: {len(payload)} bytes")

    try:
        stripe.api_key = current_app.config['STRIPE_SECRET_KEY']
        endpoint_secret = current_app.config['STRIPE_WEBHOOK_SECRET']

        logger.debug("Constructing Stripe webhook event")
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
        logger.info(f"Webhook event verified successfully: {event['type']}, ID: {event['id']}")

        if event['type'] == 'payment_intent.succeeded':
            payment_intent = event['data']['object']
            payment_intent_id = payment_intent['id']
            logger.info(f"Processing payment_intent.succeeded webhook for PaymentIntent: {payment_intent_id}")
            logger.debug(f"PaymentIntent details - Amount: {payment_intent.get('amount')}, Currency: {payment_intent.get('currency')}")

            # Update payment status in database
            payment = Payment.query.filter_by(
                stripe_payment_intent_id=payment_intent_id
            ).first()

            if payment:
                logger.info(f"Found payment record {payment.id} for PaymentIntent {payment_intent_id}, updating status to succeeded")
                payment.status = 'succeeded'
                payment.updated_at = datetime.utcnow()
                db.session.commit()
                logger.info(f"Payment {payment.id} status updated to succeeded via webhook")
            else:
                logger.warning(f"No payment record found for PaymentIntent {payment_intent_id} in webhook")

        elif event['type'] == 'payment_intent.payment_failed':
            payment_intent = event['data']['object']
            payment_intent_id = payment_intent['id']
            failure_reason = payment_intent.get('last_payment_error', {}).get('message', 'Unknown')
            logger.warning(f"Processing payment_intent.payment_failed webhook for PaymentIntent: {payment_intent_id}, reason: {failure_reason}")

            # Update payment status in database
            payment = Payment.query.filter_by(
                stripe_payment_intent_id=payment_intent_id
            ).first()

            if payment:
                logger.info(f"Found payment record {payment.id} for PaymentIntent {payment_intent_id}, updating status to failed")
                payment.status = 'failed'
                payment.updated_at = datetime.utcnow()
                db.session.commit()
                logger.warning(f"Payment {payment.id} status updated to failed via webhook, reason: {failure_reason}")
            else:
                logger.warning(f"No payment record found for PaymentIntent {payment_intent_id} in webhook")

        elif event['type'] == 'payment_intent.requires_payment_method':
            payment_intent = event['data']['object']
            logger.info(f"PaymentIntent {payment_intent['id']} requires payment method")

        elif event['type'] == 'payment_intent.processing':
            payment_intent = event['data']['object']
            logger.info(f"PaymentIntent {payment_intent['id']} is processing")

        else:
            logger.info(f"Unhandled webhook event type: {event['type']}")

        logger.debug(f"Webhook {event['id']} processed successfully")
        return jsonify({'status': 'success'})

    except ValueError as e:
        logger.error(f"Webhook payload validation error: {str(e)}")
        return jsonify({'error': 'Invalid payload'}), 400
    except stripe.error.SignatureVerificationError as e:
        logger.error(f"Webhook signature verification failed: {str(e)}")
        return jsonify({'error': 'Invalid signature'}), 400
    except Exception as e:
        logger.error(f"Unexpected error processing webhook: {str(e)}", exc_info=True)
        return jsonify({'error': 'Webhook processing failed'}), 500