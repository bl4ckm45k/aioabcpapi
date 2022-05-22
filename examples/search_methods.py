import asyncio
import logging

from loader import api, api_client

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def search_brands():
    data = await api_client.search_brands(602000800)
    logger.info(data)
    await api_client.close()


async def search_articles():
    data = await api_client.search_articles(602000600, 'Luk', 1, 1, 1)
    logger.info(data)
    await api_client.close()


async def search_bach():
    list_to_search = [{'brand': 'LuK', 'number': '602000600'}, {'brand': 'Mahle', 'number': 'OX8236D'}]
    data = await api_client.search_bach(list_to_search)
    logger.info(data)


async def search_history():
    logger.info(f'{await api_client.search_history()}')


async def advices_batch():
    positions = [{"brand": "kyb", "number": "331009"}, {"brand": "Mobil", "number": "152566"}]
    data = await api_client.advices_batch(positions)
    logger.info(data)

if __name__ == '__main__':
    try:
        asyncio.run(advices_batch())
    except RuntimeError:
        pass
