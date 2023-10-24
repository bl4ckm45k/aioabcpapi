import asyncio
import logging

from config import guest_id
from loader import api

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def get_payments_link(order_number: int, client_id: int, amount: int):
    order_payment_link = await api.cp.admin.payment.token(order_number)
    logger.info(order_payment_link)
    if client_id != int(guest_id):
        top_balance_link = await api.cp.admin.payment.top_balance_link(client_id, amount)
        logger.info(top_balance_link)


if __name__ == '__main__':
    # Необходимо только в Windows для избежания RuntimeError
    # asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    loop = asyncio.new_event_loop()
    try:
        loop.run_until_complete(get_payments_link(order_number=118668754, client_id=6679745, amount=10000))
    finally:
        loop.run_until_complete(api.close())
