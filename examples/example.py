import asyncio
import datetime
import logging
# from aiohttp import web

from loader import api
from config import guest_id

logger = logging.getLogger(__name__)


async def test_ur_request(update_start, update_end):
    data = await api.get_orders_list(
        date_updated_start=update_start,
        date_updated_end=update_end,
        format='additional')
    for x in data:
        if x['userId'] == guest_id:
            logger.info(x['additional']['phone'], x['additional']['consumer'])
    await api.close()


# async def on_startup():
#     app.add_routes([web.post(f'/web/some_path/cdek', cdek_webhook)])


if __name__ == '__main__':
    # app = web.Application()
    loop = asyncio.new_event_loop()
    date_start = (datetime.datetime.now() - datetime.timedelta(minutes=15)).strftime("%Y-%m-%d %H:%M:%S")
    date_end = (datetime.datetime.now() - datetime.timedelta(minutes=2)).strftime("%Y-%m-%d %H:%M:%S")
    loop.run_until_complete(test_ur_request(update_start=date_start, update_end=date_end))

    # loop.run_until_complete(on_startup())
    # web.run_app(app, host='127.0.0.1', port=5011)
