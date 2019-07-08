# Подключаем минимальный набор библиотек для работы
import traceback
import sys
import minimalmodbus
import asyncio
import logging
import datetime
# Подключаем библиотечный файл для отправки сообщений.
from smt.rpi.nats.messaging.CServiceMessaging import CServiceMessaging


async def kaskad():

    print(str(datetime.datetime.now()) + "Начало работы программы.")
    messaging = CServiceMessaging()

    minimalmodbus.BAUDRATE = 9600
    minimalmodbus.PARITY = 'N'
    minimalmodbus.BYTESIZE = 8
    minimalmodbus.STOPBITS = 1
    minimalmodbus.TIMEOUT = 0.1
    instrument = minimalmodbus.Instrument('/dev/ttyUSB0', slaveaddress=2,
                                          mode=minimalmodbus.MODE_RTU)  # port name, slave address (in decimal)
    instrument.debug = True

    while 1:
        try:
            logging.info(str(datetime.datetime.now()) + " Reading requested a register from controller...")
            register_demo = instrument.read_register(545, 0)  # Второй параметр: Если, 1 - 770 -> 77.0
            logging.info(str(datetime.datetime.now()) + " Successfully read a register from controller!")
            print(register_demo)
            await asyncio.ensure_future(messaging.send(register_demo))
            await asyncio.sleep(5)
        except IOError as e:
            print(str(datetime.datetime.now()) + "Failed to read from instrument. Error: ", str(e))
        except ValueError as e:
            print(str(datetime.datetime.now()) + 'Value error:', str(e))
        except TypeError as e:
            print(str(datetime.datetime.now()) + 'TypeError:', str(e))
        except Exception as e:
            print(str(datetime.datetime.now()) + 'Exception:', str(e))


async def main():
    try:
        await kaskad()
    except KeyboardInterrupt:
        # Выход из программы по нажатию Ctrl+C
        print(str(datetime.datetime.now()) + "Завершение работы Ctrl+C.")
    except Exception as e:
        # Прочие исключения
        print(str(datetime.datetime.now()) + "Ошибка в приложении.")
        # Подробности исключения через traceback
        traceback.print_exc(limit=2, file=sys.stdout)
    finally:
        print(str(datetime.datetime.now()) + "Сброс состояния порта в исходное.")
        # Информируем о завершении работы программы
        print(str(datetime.datetime.now()) + "Программа завершена.")


if __name__ == '__main__':
    asyncio.run(main())


