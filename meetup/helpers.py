import json
import os
import uuid

from yookassa import Payment, Configuration

from meetup.models import UserProfile





def check_bot_context(update, context, force_update: bool = False):
    """Обновляет состояние пользователя в контексте бота"""
    if force_update or not context.user_data.get('user'):
        user, _ = UserProfile.objects.get_or_create(
            telegram_id=update.effective_chat.id
        )
        context.user_data['user'] = user


def get_user_profile(telegram_id: int) -> UserProfile | None:
    try:
        return UserProfile.objects.get(telegram_id=telegram_id)
    except UserProfile.DoesNotExist:
        return None


def create_yoo_payment(payment_amount, payment_currency, metadata) -> dict:
    Configuration.account_id = os.environ["YOO_SHOP_ID"]
    Configuration.secret_key = os.environ["YOO_API_TOKEN"]
    if metadata is None:
        metadata = {}
    idempotence_key = str(uuid.uuid4())
    payment = Payment.create({
        "save_payment_method": True,
        "amount": {
            "value": payment_amount,
            "currency": payment_currency,
        },
        "metadata": metadata,
        "payment_method_data": {
            "type": "bank_card"
        },
        "confirmation": {
            "type": "redirect",
            "return_url": os.environ["TELEGRAM_URL"],
        },
        "capture": True,
        "description": f"Оформление подписки",
    }, idempotence_key)

    return json.loads(payment.json())
