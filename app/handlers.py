import os
import logging
from datetime import datetime, timedelta

from aiogram import Router, F, types
from aiogram.filters import CommandStart
from aiogram.types import LabeledPrice, PreCheckoutQuery, Message, FSInputFile
from aiogram import types

from app.database import set_user_paid
from app.keyboards import main_kb

router = Router()
CHANNEL_ID = os.getenv('CHANNEL_ID')

@router.message(CommandStart())
async def cmd_start(message: Message):
    photo = FSInputFile('retsuimg.jpg')
    await message.answer_photo(photo=photo,
                        caption="Добро пожаловать! \n \n [Ультра супер ахуенное описание канала] \n \n Оплатите доступ, чтобы вступить в закрытый канал.",
                        reply_markup=main_kb,
                        parse_mode='HTML')
    
@router.callback_query(F.data == "buy_access")
async def process_buy(callback: types.CallbackQuery):
    # create bill
    await callback.message.answer_invoice(
        title="Доступ в приватный канал",
        description="Единоразовый вход в закрытое сообщество",
        payload='access_payment', # user dont see this parametr, its only for you
        provider_token=os.getenv('PAYMENT_TOKEN'),
        currency="RUB",
        prices=[LabeledPrice(label='Доступ', amount=100000)], # 1000.00
        start_parameter='access_bot',
    )
    await callback.answer()

# Check while payment
@router.pre_checkout_query()
async def process_pre_checkout(pre_checkout_query: PreCheckoutQuery):
    await pre_checkout_query.answer(ok=True)


# Successful 
@router.message(F.successful_payment)
async def successful_payment(message: Message):
    try:
        
        expire_at = datetime.now() + timedelta(hours=24)
        
        # Generate link
        expire_link = await message.bot.create_chat_invite_link(
            chat_id=CHANNEL_ID,
            member_limit=1,
            expire_date=expire_at
        )

        # Save him for bd
        await set_user_paid(
            user_id=message.from_user.id,
            username=message.from_user.username
        )
    
        # Answer user
        await message.answer(
            f"✅ Оплата прошла успешно!\n\n"
            f"Ваша уникальная ссылка для входа:\n{expire_link.invite_link}\n\n"
            f"⚠️ Важно:\n"
            f"— Ссылка сработает только для 1 человека\n"
            f"— Ссылка действительна ровно 24 часа (до {expire_at.strftime('%H:%M %d.%m')})"
        )
        
    except Exception as e:
        logging.error(f"Ошибка при создании ссылки: {e}")
        
        await message.answer(
            "❌ Произошла техническая ошибка при создании ссылки.\n"
            "Не волнуйтесь, ваша оплата зафиксирована. Напишите администратору: @",
            reply_markup=None
        )
        
        await message.bot.send_message('ADMIN_ID', f"Ошибка у юзера {message.from_user.id}: {e}")