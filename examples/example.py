import asyncio
import datetime
import logging

from config import guest_id
from loader import api, api_client

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def orders_list(update_start, update_end):
    logger.info(f'{update_start}, {update_end}')
    data = await api.cp.admin.orders.get_orders_list(date_updated_start=update_start,
                                                     date_updated_end=update_end,
                                                     format='additional')

    for x in data:
        if x['userId'] == guest_id:
            logger.info(f"{x['additional']['phone']}, {x['additional']['consumer']}")
    await api.close()


async def not_enough_rights(update_start, update_end):
    data = await api_client.cp.admin.orders.get_orders_list(date_updated_start=update_start,
                                                            date_updated_end=update_end)
    logger.error(f'{data}')
    await api_client.close()


if __name__ == '__main__':
    date_start = datetime.datetime.now() - datetime.timedelta(days=3)
    date_end = datetime.datetime.now()

    # Необходимо только в Windows для избежания RuntimeError
    # asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    loop = asyncio.new_event_loop()
    try:
        loop.run_until_complete(orders_list(update_start=date_start, update_end=date_end))
    finally:
        loop.run_until_complete(api.close())
