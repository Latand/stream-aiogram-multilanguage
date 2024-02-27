from aiogram.types import User
from aiogram_i18n.managers import BaseManager


class TgUserManager(BaseManager):
    async def get_locale(self, event_from_user: User):
        return event_from_user.language_code

    async def set_locale(self, locale: str):
        pass
