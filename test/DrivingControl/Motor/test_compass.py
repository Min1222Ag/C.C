'''
import time
import board
import adafruit_bno055

i2c = board.I2C()
sensor = adafruit_bno055.BNO055_I2C(i2c)

last_val = 0xFFFF

def temperature():
    global last_val
    result = sensor.temperature
    if abs(result - last_val) == 128:
        result = sensor.temperature
        if abs(result - last_val) == 128:
            return 0b00111111 & result
    last_val = result
    return result

while True:
    print("Temperature: {} degrees C".format(temperature()))
    print("Accelerometer (m/s^2): {}".format(sensor.acceleration))
    print("Magnetometer (microteslas): {}".format(sensor.magnetic))
    print("Gyroscope (rad/sec): {}".format(sensor.gyro))
    print("Euler angle: {}".format(sensor.euler))
    print("Quaternion:: {}".format(sensor.quaternion))
    print("Linear acceleration (m/s^2): {}".format(sensor.linear_acceleration))
    print("Gravity (m/s^2): {}".format(sensor.gravity))
    print()

    time.sleep(1)
'''
import adafruit_bno055
import board

i2c = board.I2C()

sensor = adafruit_bno055.BNO055_I2C(i2c)

print(sensor.temperature)
print(sensor.euler)
print(sensor.gravity)
