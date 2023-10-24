import asyncio
import logging

from loader import api

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def search_brands():
    data = await api.cp.client.search.brands(602000800)
    logger.info(data)
    await api.close()


async def search_articles():
    data = await api.cp.client.search.articles(602000600, 'Luk',
                                               use_online_stocks=True,
                                               disable_online_filtering=True,
                                               with_out_analogs=True
                                               )
    logger.info(data)
    await api.close()


async def search_bach():
    list_to_search = [{'brand': 'LuK', 'number': '602000600'}, {'brand': 'Mahle', 'number': 'OX8236D'}]
    data = await api.cp.client.search.batch(list_to_search)
    logger.info(data)


async def search_history():
    logger.info(f'{await api.cp.client.search.history()}')


async def advices_batch():
    positions = [{"brand": "kyb", "number": "331009"}, {"brand": "Mobil", "number": "152566"}]
    data = await api.cp.client.search.advices_batch(positions)
    logger.info(data)


if __name__ == '__main__':
    # Необходимо только в Windows для избежания RuntimeError
    # asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    loop = asyncio.new_event_loop()
    try:
        loop.run_until_complete(advices_batch())
    finally:
        loop.run_until_complete(api.close())