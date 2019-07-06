# Импортируем библиотеку по работе с ModbusRTU
import traceback
import sys
import minimalmodbus
import asyncio
# Подключаем библиотечный файл для отправки сообщений.
from smt.rpi.nats.messaging.CServiceMessaging import CServiceMessaging


async def kaskad():

    print("Начало работы программы.")
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
            register_demo = instrument.read_register(545, 0)  # Номер регистра, 1 - 770 -> 77.0
            print(register_demo)
            await asyncio.ensure_future(messaging.send(register_demo))
        except IOError as e:
            print("Failed to read from instrument. Error: ", str(e))
        except ValueError as e:
            print('Value error:', str(e))
        except TypeError as e:
            print('TypeError:', str(e))
        except Exception as e:
            print('Exception:', str(e))


async def main():
    try:
        await kaskad()
    except KeyboardInterrupt:
        # Выход из программы по нажатию Ctrl+C
        print("Завершение работы Ctrl+C.")
    except Exception as e:
        # Прочие исключения
        print("Ошибка в приложении.")
        # Подробности исключения через traceback
        traceback.print_exc(limit=2, file=sys.stdout)
    finally:
        print("Сброс состояния порта в исходное.")
        # Информируем о завершении работы программы
        print("Программа завершена.")


if __name__ == '__main__':
    asyncio.run(main())
    # ioloop = asyncio.get_event_loop()
    # tasks = [ioloop.create_task(main())]
    # wait_tasks = asyncio.wait(tasks)
    # ioloop.run_until_complete(wait_tasks)
    # ioloop.close()


