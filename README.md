## AioAbcpApi

Асинхронная библиотека для [API ABCP](https://www.abcp.ru/wiki/ABCP.API "API ABCP")
с [asyncio](https://docs.python.org/3/library/asyncio.html "asyncio")
и [aiohttp](https://github.com/aio-libs/aiohttp "aiohttp")

![](https://img.shields.io/github/stars/bl4ckm45k/aioabcpapi.svg)
![](https://img.shields.io/github/forks/bl4ckm45k/aioabcpapi.svg)
![](https://img.shields.io/github/issues/bl4ckm45k/aioabcpapi.svg)
[![Supported python versions](https://img.shields.io/pypi/pyversions/aioabcpapi.svg)](https://pypi.python.org/pypi/aioabcpapi)
[![Downloads](https://img.shields.io/pypi/dm/aioabcpapi.svg?)](https://pypi.python.org/pypi/aioabcpapi)
[![PyPi Package Version](https://img.shields.io/pypi/v/aioabcpapi)](https://pypi.python.org/pypi/aioabcpapi)


Присоединяйтесь к [телеграм чату](https://t.me/aioabcpapi "Телеграм чат")
### Установка
`pip install aioabcpapi`

### Описание

------------

Все методы максимально приближены к древовидному оформлению [официальной документации](https://www.abcp.ru/wiki/ABCP.API).

Разделяются на `cp` и `ts`, они в свою очередь разделяются на `client` и `admin`, далее для поиска нужного вам метода
отталкивайтесь от документации [API ABCP](https://www.abcp.ru/wiki/ABCP.API).

Для примера, из документации **TS.Client**, [Обновление позиции в корзине](https://www.abcp.ru/wiki/API.TS.Client#.D0.9E.D0.B1.D0.BD.D0.BE.D0.B2.D0.BB.D0.B5.D0.BD.D0.B8.D0.B5_.D0.BF.D0.BE.D0.B7.D0.B8.D1.86.D0.B8.D0.B8_.D0.B2_.D0.BA.D0.BE.D1.80.D0.B7.D0.B8.D0.BD.D0.B5)
описание операции следующее:
>  Операция: POST /ts/cart/update

Для использования этого метода нам нужно будет обратиться к `await api.ts.client.cart.update()`

### Доступ к API

------------
[Для API Администратора](https://cp.abcp.ru/?page=allsettings&systemsettings&apiInformation)

Если вы являетесь клиентом магазина на платформе ABCP, обратитесь к вашему менеджеру. (Вам понадобится статический IP адрес)

### Примечание 

------------

Все аргументы времени, такие как `create_time`, `update_time`, `date_start`, `date_end` и прочие, принимают `str` или `datetime`. При передаче `datetime` объект будет преобразован в зависимости от требований метода в `RFC3339` или `"%Y-%m-%d %H:%M:%S"`

### Пример

------------

```python
import asyncio
from aioabcpapi import Abcp

host, login, password = 'id33333', 'api@id33333', 'md5hash'
api = Abcp(host, login, password)


async def search_some_parts(article, brand):
    search_result = await api.cp.client.search.articles(number=article, brand=brand,
                                                        use_online_stocks=True,
                                                        disable_online_filtering=True,
                                                        with_out_analogs=True)
    for x in search_result:
        if float(x['price']) < 3000:
            print('Похоже на чудо, но скорее ошибка прайса. Отключим пока поставщика')
            await api.cp.admin.distributors.edit_status(x['distributorId'], False)
        elif float(x['price']) < 37000:
            await api.cp.client.basket.add(basket_positions={'number': x['article'],
                                                             'brand': x['brand'],
                                                             'supplierCode': x['supplierCode'],
                                                             'itemKey': x['itemKey'],
                                                             'quantity': 1,
                                                             'comment': f"Да, РРЦ никто не любит"})


if __name__ == '__main__':
    asyncio.run(search_some_parts('602000600', 'LuK'))
```

[**Больше примеров**](https://github.com/bl4ckm45k/aioabcpapi/tree/master/examples "Примеры")