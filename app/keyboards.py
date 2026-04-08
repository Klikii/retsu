from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

main_kb = InlineKeyboardMarkup(inline_keyboard=
            [
                [InlineKeyboardButton(text="💎 Оплатить доступ (1000₽)", callback_data='buy_access')],
                [InlineKeyboardButton(text="ℹ️ Информация", callback_data='info')],
                [InlineKeyboardButton(text="🆘 Поддержка", url='https://t.me')],
            ])