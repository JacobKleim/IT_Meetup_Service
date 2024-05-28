import uuid

from yookassa import Payment

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


