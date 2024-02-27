import asyncio
import logging

import betterlogging as bl
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram_i18n import I18nMiddleware
from aiogram_i18n.cores.fluent_runtime_core import FluentRuntimeCore

from tgbot.config import load_config
from tgbot.handlers import routers_list
from tgbot.middlewares.translations import TgUserManager


def setup_logging():
    log_level = logging.INFO
    bl.basic_colorized_config(level=log_level)

    logging.basicConfig(
        level=logging.INFO,
        format="%(filename)s:%(lineno)d #%(levelname)-8s [%(asctime)s] - %(name)s - %(message)s",
    )
    logger = logging.getLogger(__name__)
    logger.info("Starting bot")


async def main():
    setup_logging()

    config = load_config(".env")

    bot = Bot(token=config.tg_bot.token, parse_mode="HTML")
    dp = Dispatcher(storage=MemoryStorage())
    i18n_middleware = I18nMiddleware(
        core=FluentRuntimeCore(path="tgbot/locales"),
        default_locale="uk",
        manager=TgUserManager(),
    )

    dp.include_routers(*routers_list)
    dp.workflow_data.update(config=config)
    i18n_middleware.setup(dp)

    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logging.error("Бот був вимкнений!")
