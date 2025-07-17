import requests
import os
import asyncio
import time

import logging

from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
from aiogram.enums.parse_mode import ParseMode
from aiogram.types.inline_keyboard_button import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

logging.basicConfig(level=logging.INFO)

# proxies = os.getenv('PROXIES')

bot = Bot(mytokenbot)
dp = Dispatcher()


def get_category():
    url = 'https://catalog.wb.ru/catalog/electronic14/v2/catalog?ab_testing=false&appType=1&cat=9468&curr=rub&dest=-1185367&sort=popular&spp=30'

    headers = {
        'Accept': '*/*',
        'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
        'Connection': 'keep-alive',
        'DNT': '1',
        'Origin': 'https://www.wildberries.ru',
        'Referer': 'https://www.wildberries.ru/catalog/elektronika/igry-i-razvlecheniya/aksessuary/garnitury',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'cross-site',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36',
        'sec-ch-ua': '"Not)A;Brand";v="99", "Google Chrome";v="127", "Chromium";v="127"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
    }

    response = requests.get(url=url, headers=headers)

    return response.json()


def format_items(response):
    products = []

    products_raw = response.get('data', {}).get('products', None)

    if products_raw != None and len(products_raw) > 0:
        for product in products_raw:
            products.append({
                'brand': product.get('brand', None),
                'name': product.get('name', None),
                'id': product.get('id', None),
                'reviewRating': product.get('reviewRating', None),
                'feedbacks': product.get('feedbacks', None),
            })

    return products


@dp.message(CommandStart)
async def start(message: types.Message):
    response = get_category()
    products = format_items(response)

    items = 0

    for product in products:
        text = f"<b>Категория</b>: Гарнитуры и наушники\n\n<b>Название</b>: {product['name']}\n<b>Бренд</b>: {product['brand']}\n\n<b>Отзывов всего</b>: {product['feedbacks']}\n<b>Средняя оценка</b>: {product['reviewRating']}"

        builder = InlineKeyboardBuilder()
        builder.add(
            InlineKeyboardButton(text="Открыть", url=f"https://www.wildberries.ru/catalog/{product['id']}/detail.aspx"))

        await message.answer(text, parse_mode=ParseMode.HTML, reply_markup=builder.as_markup())

        if items >= 10:
            break
        items += 1

        time.sleep(0.3)


async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())