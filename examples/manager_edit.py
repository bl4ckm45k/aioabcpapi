import asyncio
import logging

from loader import api

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


async def update_manager(id, first_name, last_name, sip):
    update_result = await api.cp.admin.staff.update_manager(id, first_name=first_name, last_name=last_name, sip=sip)
    logger.info(update_result)


if __name__ == '__main__':
    # Необходимо только в Windows для избежания RuntimeError
    # asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    loop = asyncio.new_event_loop()
    try:
        loop.run_until_complete(update_manager(id=25119353, first_name='test_first', last_name='test_last', sip=312))
    finally:
        loop.run_until_complete(api.close())
