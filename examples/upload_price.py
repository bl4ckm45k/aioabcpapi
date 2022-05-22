import asyncio
import logging

from loader import api

logger = logging.getLogger(__name__)


async def example_upload_price_list(distributor_id, file_path):
    data = await api.pricelist_update(distributor_id, file_path)
    logger.info(data)


if __name__ == '__main__':
    loop = asyncio.new_event_loop()
    import os

    cwd = os.getcwd()
    files = os.listdir('files')
    distributors = [1642117]
    for i in range(len(files)):
        loop.run_until_complete(example_upload_price_list(distributor_id=distributors[i],
                                                          file_path=open(f'{cwd}/files/{files[i]}', 'rb')))
        # loop.run_until_complete(example_upload_price_list(distributor_id=1642117,
        #                                                   file_path=f'{cwd}/files/{files[i]}'))
