# *******************************************************************************************************
# Класс содержит методы для обмена сообщениями чере сервер NATS.                                        *
# @author Селетков И.П. 2018 1214.                                                                      *
# *******************************************************************************************************
import asyncio
import logging
from nats.aio.client import Client as NATSClientLibrary
from nats.aio.errors import ErrNoServers


class CServiceMessaging:
    # Путь к конфигурационным настройкам параметров системы
    path = "settings1.ini"

    # ***************************************************************************************************
    # Конструктор объекта.                                                                              *
    # ***************************************************************************************************
    def __init__(self):
        logging.basicConfig(level=logging.DEBUG)
        self.__nc = NATSClientLibrary()

    # ***************************************************************************************************
    # Подключение к серверу NATS + оформление подписки на получение сообщений от пользователей          *
    # ***************************************************************************************************
    async def __connect(self):
        if not self.__nc.is_connected:
            logging.info(" Establishing connection to NATS server.")
            try:
                await self.__nc.connect("192.168.1.104", loop=asyncio.get_running_loop())
                # await self.__nc.connect("192.168.1.104", loop=asyncio.get_event_loop())
                logging.info(" Connection to NATS server is established.")
                # await CServiceMessaging.receive(self)
                # logging.info("Created receiver messages from the server NATS")
            except ErrNoServers as e:
                logging.error(" Cannot connect to NATS server.", e)

    # ***************************************************************************************************
    # Отправка сообщения на сервер NATS.                                                                *
    # ***************************************************************************************************
    async def send(self, message):
        await self.__connect()
        if not self.__nc.is_connected:
            return
        try:
            # await self.__nc.publish("TEMP_IN_DEVICE_FROM_SERVER", message.encode("UTF-8"))
            logging.info(" Publishing the message by subject.")
            await self.__nc.publish("TEMP_IN_DEVICE_FROM_SERVER", bytes(message))
            logging.info(" Message was successfully published!")
        except Exception as e:
            logging.error(" Exception.", e)

    # ***************************************************************************************************
    # Завершение работы, закрытие соединения с сервером.                                                *
    # ***************************************************************************************************
    async def close(self):
        if not self.__nc.is_connected:
            return
        logging.info(" Closing connection to NATS server.")
        await self.__nc.close()
        logging.info(" Connection to NATS server closed.")

    # # ***************************************************************************************************
    # # Получение сообщения с сервера NATS.                                                               *
    # # ***************************************************************************************************
    # async def receive(self):
    #     if not self.__nc.is_connected:
    #         return
    #
    #     async def message_handler(msg):
    #         data = json.loads(msg.data.decode())
    #
    #         uuid = data['UUID']
    #         obj_meas = data['ObjectMeasure']
    #         cur_time = data['CurrentTime']
    #         delay_temp = data['Delay']
    #
    #         CServiceMessaging.change_delay(delay_temp, 0)
    #
    #         print(data)
    #
    #     await self.__nc.subscribe("TEMP_FROM_DEVICE_TO_SERVER", cb=message_handler)

    # # ***************************************************************************************************
    # # Обновление частоты опроса датчика                                                                 *
    # # ***************************************************************************************************
    # def change_delay(param_delay, param_num):
    #     if param_num == 0:
    #         CConfigManager.update_setting(CServiceMessaging.path, "Settings", "timedelay", str(param_delay/2))
    #     if param_num == 1:
    #         return CConfigManager.get_setting(CServiceMessaging.path, "Settings", "timedelay")

    # # ***************************************************************************************************
    # # Обновление данных с датчика                                                               *
    # # ***************************************************************************************************
    # async def refresh(self):
    #     if not self.__nc.is_connected:
    #         return
    #
    #     async def message_handler(msg):
    #         # Инициализация пинов для датчика температуры: rst, dq, clk
    #         t_sensor = DS1620(17, 18, 27)
    #         # Считываем температуру
    #         temperature = t_sensor.get_temperature()
    #         await self.__nc.publish(msg.reply, json.dumps({"ObjectMeasure": "Temperature", "Data": temperature}).encode())
    #
    #     await self.__nc.subscribe("TEMP_IN_DEVICE_FROM_SERVER_UPD", cb=message_handler)
