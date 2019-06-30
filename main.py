# Импортируем библиотеку по работе с ModbusRTU
import struct
import time
import minimalmodbus
# Импортируем библиотеку по работе с GPIO
import RPi.GPIO as GPIO


def kaskad():
    import serial
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(11, GPIO.OUT)
    GPIO.setup(15, GPIO.OUT)

    serial = serial.Serial(
        port='/dev/ttyAMA0',
        baudrate=9600,
        parity=serial.PARITY_NONE,
        bytesize=serial.EIGHTBITS,
        stopbits=serial.STOPBITS_ONE,
        timeout=0.5,
        rtscts=True
    )

    print('Connected:', serial.isOpen())
    print("Connected to: " + serial.portstr)

    GPIO.output(11, GPIO.LOW)  # set high/transmit
    GPIO.output(15, GPIO.HIGH)  # set high/transmit
    data = '0203024800010597'
    b = bytes.fromhex(data)
    print("Writing...")
    serial.write(b)
    print("Written.")
    GPIO.output(11, GPIO.HIGH)  # pin set to low/receive
    GPIO.output(15, GPIO.LOW)  # pin set to low/receive
    ReceivedData = ""
    while ReceivedData == "":
        RecievedData = serial.readline()
        print(ReceivedData)

    # minimalmodbus.BAUDRATE = 9600
    # minimalmodbus.PARITY = 'N'
    # minimalmodbus.BYTESIZE = 8
    # minimalmodbus.STOPBITS = 1
    # minimalmodbus.TIMEOUT = 0.25
    # instrument = minimalmodbus.Instrument('/dev/ttyAMA0', slaveaddress=2,
    #                                       mode='rtu')  # port name, slave address (in decimal)
    # instrument.debug = True
    # while(True):
    #     try:
    #         temperature = instrument.read_registers(registeraddress=257,
    #                                                 numberOfRegisters=4, functioncode=4)  # Register number, number of decimals
    #         print(temperature)
    #     except IOError as e:
    #         print("Failed to read from instrument. Error: ", str(e))
    #     except Exception as e:\
    #         print('Error zapros:', str(e))


if __name__ == '__main__':
    kaskad()
