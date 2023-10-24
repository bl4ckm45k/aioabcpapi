import asyncio
import logging

from loader import api

logger = logging.getLogger(__name__)


async def get_basket_params():
    options = await api.cp.client.basket.options()
    payment = await api.cp.client.basket.payment_method()
    shipment = await api.cp.client.basket.shipment_method()
    addresses = await api.cp.client.basket.shipment_address()
    offices = await api.cp.client.basket.shipment_offices()
    logger.info(f'{options}\n{payment}\n{shipment}\n{addresses}\n{offices}')

    # Прочтите аннотации к методу перед использованием
    await api.cp.client.basket.set_client_params(payment_method_index=0,
                                                 shipment_address_index=0,
                                                 shipment_office_index=0)
    orders_list = await api.cp.client.orders.orders_list(
        orders=[94233131, 93745568]
    )
    logger.info(f'{orders_list}')


if __name__ == '__main__':
    # Необходимо только в Windows для избежания RuntimeError
    # asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    loop = asyncio.new_event_loop()
    try:
        loop.run_until_complete(get_basket_params())
    finally:
        loop.run_until_complete(api.close())
