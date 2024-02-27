from typing import TYPE_CHECKING

from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.filters.callback_data import CallbackData
from aiogram.types import CallbackQuery, Message
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram_i18n.context import I18nContext

if TYPE_CHECKING:
    from tgbot.stub.stub import I18nContext

user_router = Router()


class LanguageCD(CallbackData, prefix="lang"):
    lang: str


def language_kb(i18n: I18nContext):
    kb = InlineKeyboardBuilder()
    kb.button(text=i18n.languages.uk(), callback_data=LanguageCD(lang="uk"))
    kb.button(text=i18n.languages.en(), callback_data=LanguageCD(lang="en"))
    kb.adjust(1)
    return kb.as_markup()


@user_router.message(CommandStart())
async def user_start(message: Message, i18n: I18nContext):
    # await message.reply("Вітаю, звичайний користувач!")
    await message.reply(i18n.user.start_cmd(), reply_markup=language_kb(i18n))
    # for number in random.sample(range(1, 100), 5):
    # await message.answer(i18n.random.number(number=number))
    # await asyncio.sleep(1)

    for gender in ["male", "female", "trans"]:
        await message.answer(i18n.gender.info(gender=gender))


@user_router.callback_query(LanguageCD.filter())
async def set_new_language(
    callback_query: CallbackQuery, callback_data: LanguageCD, i18n: I18nContext
):
    await callback_query.answer()
    await i18n.set_locale(callback_data.lang)

    await callback_query.message.answer(
        i18n.user.language_changed(), reply_markup=language_kb(i18n)
    )
