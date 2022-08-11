import asyncio
import logging

from loader import api

logger = logging.getLogger(__name__)


async def example_upload_price_list(distributor_id, file_or_path):
    # В данном методе аргуемент file_or_path может принимать как путь к файлу так и откытый файл.
    # Открытый файл будет закрыт еще до отправки запроса к API
    data = await api.cp.admin.distributors.pricelist_update(distributor_id=distributor_id, file_or_path=file_or_path)
    logger.info(data)


if __name__ == '__main__':
    import os

    cwd = os.getcwd()
    files = os.listdir('files')
    distributors = [1642117]
    for i in range(len(files)):
        asyncio.run(example_upload_price_list(distributor_id=distributors[i],
                                              file_or_path=open(f'{cwd}/files/{files[i]}', 'rb')))
        # asyncio.run(example_upload_price_list(distributor_id=1642117,
        #                                       file_or_path=f'{cwd}/files/{files[i]}'))
