from fastapi import APIRouter, Depends, HTTPException, Request, Header
import stripe
from firebase_admin import auth
from database.firebase import db
from fastapi.security import OAuth2PasswordBearer
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from classes.schema_dto import User

router = APIRouter(
    tags=["Stripe"],
    prefix='/stripe'
)

# Endpoint pour créer une session de paiement Stripe
@router.get('/checkout')
async def stripe_checkout(user: User = Depends(get_current_user)):
    try:
        checkout_session = stripe.checkout.Session.create(
            line_items=[
                {
                    'price': 'price_1O4KaQDeNOaTDGEGg4CeNuUE',
                },
            ],
            mode='subscription',
            payment_method_types=['card'],
            success_url='YOUR_SUCCESS_URL',  # Remplacez par votre URL de succès
            cancel_url='YOUR_CANCEL_URL',  # Remplacez par votre URL d'annulation
            client_reference_id=user.email  # Utilisez l'e-mail de l'utilisateur comme référence
        )
        return {"checkout_url": checkout_session['url']}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Endpoint pour gérer les webhooks Stripe
@router.post('/webhook')
async def webhook_received(request: Request, stripe_signature: str = Header(None)):
    webhook_secret = "whsec_f6de37ea1d173a3db4295ec622b17c148f71829c171080078c73e35ef0f64065"  # Remplacez par votre secret de webhook Stripe
    data = await request.body()
    try:
        event = stripe.Webhook.construct_event(
            payload=data,
            sig_header=stripe_signature,
            secret=webhook_secret
        )
        # Traitez l'événement Stripe ici
        handle_stripe_event(event)
    except stripe.error.SignatureVerificationError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    return {"status": "success"}

# Fonction pour gérer les événements Stripe
def handle_stripe_event(event):
    event_type = event['type']
    if event_type == 'checkout.session.completed':
        print('Checkout session completed')
    elif event_type == 'invoice.paid':
        print('Invoice paid')
    elif event_type == 'invoice.payment_failed':
        print('Invoice payment failed')

