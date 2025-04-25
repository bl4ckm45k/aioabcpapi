import asyncio
from loader import api


# from aioabcpapi import Abcp

# api = Abcp('host', 'login', 'password')

async def async_context_manager():
    """
    Пример использования библиотеки ABCP API
    Поиск товаров и добавление в корзину

    Использование через контекстный менеджер - сессия закроется автоматически
    """

    async with api:
        # Поиск товаров
        search_result = await api.cp.client.search.articles(
            number='602000600',
            brand='LuK',
            use_online_stocks=True,
            disable_online_filtering=True,
            with_out_analogs=True
        )

        print(f"Найдено товаров: {len(search_result)}")
        sorted_search_result = sorted(search_result, key=lambda x: x['price'])
    # Фильтрация и обработка результатов
    for item in sorted_search_result:
        price = float(item['price'])
        print(f"Артикул: {item['numberFix']}, Бренд: {item['brand']}, Цена: {price}")
        if price < 3000:
            print('Похоже на ошибку в прайсе. Отключаем поставщика временно.')
            # Отключаем поставщика с подозрительно низкой ценой
            async with api:
                result = await api.cp.admin.distributors.edit_status(item['distributorId'], False)
                print(f"Результат отключения поставщика: {result}")
        elif price < 45000:
            # Добавляем товар в корзину
            async with api:
                result = await api.cp.client.basket.add(
                    basket_positions={
                        'number': item['article'],
                        'brand': item['brand'],
                        'supplierCode': item['supplierCode'],
                        'itemKey': item['itemKey'],
                        'quantity': 1,
                        'comment': "РРЦ никто не любит"
                    }
                )

                print(f"Результат добавляение в корзину: {result}")


async def wo_async_context_manager():
    """
    Пример использования библиотеки ABCP API
    Поиск товаров и добавление в корзину

    Использование без контекстного менеджера - закрывайте сессию самостоятельно
    """

    # Поиск товаров
    search_result = await api.cp.client.search.articles(
        number='602000600',
        brand='LuK',
        use_online_stocks=True,
        disable_online_filtering=True,
        with_out_analogs=True
    )

    print(f"Найдено товаров: {len(search_result)}")
    sorted_search_result = sorted(search_result, key=lambda x: x['price'])
    # Фильтрация и обработка результатов
    for item in sorted_search_result:
        price = float(item['price'])
        print(f"Артикул: {item['numberFix']}, Бренд: {item['brand']}, Цена: {price}")
        if price < 3000:
            print('Похоже на ошибку в прайсе. Отключаем поставщика временно.')
            # Отключаем поставщика с подозрительно низкой ценой
            result = await api.cp.admin.distributors.edit_status(item['distributorId'], False)
            print(f"Результат отключения поставщика: {result}")
        elif price < 45000:
            # Добавляем товар в корзину
            result = await api.cp.client.basket.add(
                basket_positions={
                    'number': item['article'],
                    'brand': item['brand'],
                    'supplierCode': item['supplierCode'],
                    'itemKey': item['itemKey'],
                    'quantity': 1,
                    'comment': "РРЦ никто не любит"
                }
            )

            print(f"Результат добавляение в корзину: {result}")

    await api.close()

if __name__ == '__main__':
    # Запуск примеров
    asyncio.run(async_context_manager())
    asyncio.run(wo_async_context_manager())