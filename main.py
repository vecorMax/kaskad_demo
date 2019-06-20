# Импортируем библиотеку по работе с ModbusRTU
import struct
import time

# Импортируем библиотеку по работе с GPIO
import RPi.GPIO as GPIO
import minimalmodbus


def kaskad():
    import serial
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(12, GPIO.OUT)

    serial = serial.Serial(
        port='/dev/ttyAMA0',
        baudrate=9600,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
        timeout=0.05,
        rtscts=True
    )

    print('Connected:', serial.isOpen())
    print("Connected to: " + serial.portstr)

    GPIO.output(12, 0)  # set high/transmit
    # ByteStringToSend = "\x00\x01\x04\x01\x01\x00\x04\xA1\xF5"
    # str1 = str.encode(ByteStringToSend)
    # byt = bytes.decode(str1)
    data = '010401050004A1F5'
    b = bytes.fromhex(data)
    print("Writing...")
    serial.write(b)
    print("Written.")
    time.sleep(0.5)  # baud for 9600
    GPIO.output(12, 1)  # pin set to low/receive
    ReceivedData = ""
    while (ReceivedData == ""):
        RecievedData = serial.readline();
        print(RecievedData.enc)

    minimalmodbus.BAUDRATE = 9600
    instrument = minimalmodbus.Instrument('/dev/ttyAMA0', 2)  # port name, slave address (in decimal)
    temperature = instrument.read_register(262, 0, 3)  # Register number, number of decimals
    print(temperature)


if __name__ == '__main__':
    kaskad()
