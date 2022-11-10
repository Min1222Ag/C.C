import serial
import adafruit_bno055
uart = serial.Serial("/dev/serial0")
sensor = adafruit_bno055.BNO055_UART(uart)

