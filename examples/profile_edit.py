from loader import api
import asyncio
import logging

logger = logging.getLogger(__name__)


async def edit_profile():
    data = await api.cp.admin.users.edit_profile(profile_id=76423899, price_up=0,
                                                 matrix_price_ups=[{'from': 0,
                                                                    'to': 20,
                                                                    'priceUp': 450},
                                                                   {'from': 20,
                                                                    'to': 200,
                                                                    'priceUp': 60},
                                                                   {'from': 200,
                                                                    'to': 100,
                                                                    'priceUp': 40}
                                                                   ],
                                                 distributors_price_ups={
                                                     'id': 1586062,
                                                     'isEnabled': 1,
                                                     'priceUp': 0,
                                                     'brandsPriceUps': {'Airtex': '9', 'Ajusa': '8', 'Akebono': '9',
                                                                        'Attex': '9', 'Autopartner': '8', 'Ava': '7',
                                                                        'B CAR': '9', 'BIG FILTER': '8', 'BIZOL': '9',
                                                                        'CARLINE': '9', 'CS Germany': '9', 'CTR': '9',
                                                                        'CX': '9', 'Car-dex': '8', 'Chamaleon': '9',
                                                                        'Champion': '9', 'Clean filters': '9',
                                                                        'ContiTech': '7', 'Corteco': '10', 'Dashi': '8',
                                                                        'Dayco': '9', 'Delphi': '9',
                                                                        'LUCKY WAY': '5', 'LUZAR': '9', 'LYNXauto': '9',
                                                                        'Liqui moly': '5', 'Lucas': '5.5', 'Luk': '5.5',
                                                                        'MANN-FILTER': '8', 'MARSHALL': '5',
                                                                        'MEAT & DORIA': '6.5', 'MERCEDES-BENZ': '8',
                                                                        'Mahle/Knecht': '8', 'Malo': '9', 'Mando': '8',
                                                                        'NiBK': '8', 'OPEL': '13', 'OPET': '9',
                                                                        'OSVAT': '8', 'PARTRA': '8', 'PERSEA': '9',
                                                                        'PETRO-CANADA': '5', 'PURFLUX': '14',
                                                                        'Parts-Mall': '7', 'Payen': '6.5',
                                                                        'Philips': '7', 'Polmostrow': '0', 'RC': '11',
                                                                        'REIN': '5', 'RENAULT': '9', 'RODRUNNER': '9',
                                                                        'RUSEFF': '5', 'Raon': '9', 'Rosneft': '9',
                                                                        'Ruville': '9', 'SENATOR': '9', 'SIM': '5',
                                                                        'Sachs': '10', 'Sakura': '12', 'Shaftec': '9',
                                                                        'Sidem': '6.5', 'Siger': '9', 'Skf': '9',
                                                                        'Swf': '5', 'TESLA': '5', 'TMI TATSUMI': '3',
                                                                        'TORR': '9', 'TOTEM LINERS': '5', 'TOYOTA': '9',
                                                                        'TRANSMASTER UNIVERSAL': '8',
                                                                        'TRANSMASTER': '8', 'TRW': '5.5', 'TSN': '9',
                                                                        'Teknorot': '9', 'Textar': '9', }

                                                 })

    logger.info(f'{data}')


if __name__ == '__main__':
    asyncio.run(edit_profile())
