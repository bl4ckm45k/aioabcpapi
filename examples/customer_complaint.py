import asyncio
import os

from loader import api
import logging

logging.basicConfig(level=logging.DEBUG)
logging = logging.getLogger(__name__)


async def get_complaints():
    data = await api.ts.admin.customer_complaints.get(32)
    logging.info(f'{data}')


async def update_complaint(path_to_file):
    # Данный метод поддерживает только передачу пути к файлу.
    # Он сам преобразует файл в base64
    data = await api.ts.admin.customer_complaints.update(32, 32, 25090387, custom_complaint_file=path_to_file)
    logging.info(f"{data}")


if __name__ == '__main__':
    cwd = os.getcwd()
    path_to_some_file = f'{cwd}/files/some_file.txt'
    asyncio.run(update_complaint(path_to_some_file))
