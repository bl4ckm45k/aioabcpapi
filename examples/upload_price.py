import asyncio
import logging

from loader import api

logger = logging.getLogger(__name__)


async def example_upload_price_list(distributor_id, upload_file):
    # В данном методе аргуемент upload_file может принимать как путь к файлу так и откытый файл.
    # Открытый файл будет закрыт еще до отправки запроса к API
    data = await api.cp.admin.distributors.pricelist_update(distributor_id=distributor_id, upload_file=upload_file)
    logger.info(data)


if __name__ == '__main__':
    import os

    cwd = os.getcwd()
    files = os.listdir('files')
    distributors = [1642117]
    for i in range(len(files)):
        asyncio.run(example_upload_price_list(distributor_id=1642117,
                                              upload_file=f'{cwd}/files/{files[i]}'))
        # asyncio.run(example_upload_price_list(distributor_id=distributors[i],
        #                                       upload_file=open(f'{cwd}/files/{files[i]}', 'rb')))

