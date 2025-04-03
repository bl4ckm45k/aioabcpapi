import asyncio
from datetime import datetime, timedelta

from aioabcpapi import Abcp


async def search_and_add_to_basket():
    """
    Пример использования библиотеки ABCP API
    Поиск товаров и добавление в корзину
    """
    host, login, password = 'id33333', 'api@id33333', 'md5hash'
    
    # Использование через контекстный менеджер - сессия закроется автоматически
    async with Abcp(host, login, password) as api:
        # Поиск товаров
        search_result = await api.cp.client.search.articles(
            number='602000600',
            brand='LuK',
            use_online_stocks=True,
            disable_online_filtering=True,
            with_out_analogs=True
        )
        
        print(f"Найдено {len(search_result)} товаров")
        
        # Фильтрация и обработка результатов
        for item in search_result:
            price = float(item['price'])
            print(f"Артикул: {item['article']}, Бренд: {item['brand']}, Цена: {price}")
            
            if price < 3000:
                print('Похоже на ошибку в прайсе. Отключаем поставщика временно.')
                # Отключаем поставщика с подозрительно низкой ценой
                await api.cp.admin.distributors.edit_status(item['distributorId'], False)
            elif price < 37000:
                # Добавляем товар в корзину
                await api.cp.client.basket.add(
                    basket_positions={
                        'number': item['article'],
                        'brand': item['brand'],
                        'supplierCode': item['supplierCode'],
                        'itemKey': item['itemKey'],
                        'quantity': 1,
                        'comment': "РРЦ никто не любит"
                    }
                )
                print(f"Товар добавлен в корзину: {item['article']} {item['brand']}")


async def get_recent_orders():
    """
    Пример получения недавних заказов
    с использованием параметров даты
    """
    host, login, password = 'id33333', 'api@id33333', 'md5hash'
    
    # Создание экземпляра API с настройками таймаута и ретраев
    api = Abcp(
        host=host, 
        login=login, 
        password=password,
        timeout=30,  # 30 секунд таймаут
        retry_attempts=5,  # 5 попыток при ошибках
        retry_delay=0.5  # Задержка между попытками 0.5 секунды
    )
    
    try:
        # Получаем заказы за последние 7 дней
        date_from = datetime.now() - timedelta(days=7)
        date_to = datetime.now()
        
        orders = await api.cp.client.garage.get_orders(
            date_from=date_from,
            date_to=date_to,
            limit=10
        )
        
        print(f"Заказы за последние 7 дней: {len(orders)}")
        for order in orders:
            print(f"Заказ №{order['orderId']} от {order['createDate']} - {order['statusName']}")
    
    finally:
        # Важно всегда закрывать сессию, если не используете контекстный менеджер
        await api.close()


if __name__ == '__main__':
    # Запуск примеров
    asyncio.run(search_and_add_to_basket())
    asyncio.run(get_recent_orders())
