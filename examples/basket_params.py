import asyncio
import logging

from loader import api_client

logger = logging.getLogger(__name__)


async def get_basket_params():
    options = await api_client.basket_options()
    payment = await api_client.basket_payment_method()
    shipment = await api_client.basket_shipment_method()
    addresses = await api_client.basket_shipment_address()
    offices = await api_client.basket_shipment_offices()
    logger.info(f'\n{options}\n{payment}\n{shipment}\n{addresses}\n{offices}')

    # Прочтите аннотации к методу перед использованием
    await api_client.set_client_params(
        payment_method_index=0,
        shipment_address_index=0,
        shipment_office_index=0
    )
    orders_list = await api_client.get_orders_list(orders=[94233131,
                                                    93745568])
    logger.info(f'{orders_list}')


if __name__ == '__main__':
    asyncio.run(get_basket_params())
