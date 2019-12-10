#
# Get Humidity
#
# v0.0.1
#

import RPi.GPIO as GPIO
import time
import logging

SENSOR_VALUE_AIR = 158
SENSOR_VALUE_WATER = 41
START = 37  # Start pin
INTR = 22  # INTR pin
DATA0 = 29  # Data pin
DATA1 = 31  # Data pin
DATA2 = 33  # Data pin
DATA3 = 35  # Data pin
DATA4 = 32  # Data pin
DATA5 = 36  # Data pin
DATA6 = 38  # Data pin
DATA7 = 40  # Data pin
SENSOR_VCC = 7  # Humidity sensor's Vcc pin
TURN_ON_SENSOR = GPIO.HIGH
TURN_OFF_SENSOR = GPIO.LOW

try:
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    new_humidity = 0

    def get_humidity_percent(humidity):
        if humidity > SENSOR_VALUE_AIR:
            return 0
        if humidity < SENSOR_VALUE_WATER:
            return 100
        return (SENSOR_VALUE_AIR - humidity) * 100 / (SENSOR_VALUE_AIR - SENSOR_VALUE_WATER)

    def get_humidity_value(chn):
        GPIO.output(START, GPIO.LOW)
        time.sleep(0.001)
        GPIO.output(START, GPIO.HIGH)
        data = 0
        if GPIO.input(DATA0):
            data += 2**0
        if GPIO.input(DATA1):
            data += 2**1
        if GPIO.input(DATA2):
            data += 2**2
        if GPIO.input(DATA3):
            data += 2**3
        if GPIO.input(DATA4):
            data += 2**4
        if GPIO.input(DATA5):
            data += 2**5
        if GPIO.input(DATA6):
            data += 2**6
        if GPIO.input(DATA7):
            data += 2**7
        # Get the last received value from the Sensor only when it's turned on
        if GPIO.input(SENSOR_VCC) == TURN_ON_SENSOR:
            global new_humidity

            new_humidity = data

    # Configure GPIO
    logger.info('Configurando GPIO...')
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(INTR, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(START, GPIO.OUT)
    GPIO.setup(SENSOR_VCC, GPIO.OUT)
    GPIO.setup(DATA0, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(DATA1, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(DATA2, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(DATA3, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(DATA4, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(DATA5, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(DATA6, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(DATA7, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

    GPIO.add_event_detect(INTR, GPIO.FALLING, get_humidity_value)

    # Starting A/D
    logger.info('Starting A/D...')
    GPIO.output(START, GPIO.HIGH)
    time.sleep(0.001)
    GPIO.output(START, GPIO.LOW)
    time.sleep(0.001)
    GPIO.output(START, GPIO.HIGH)
    time.sleep(0.001)

    printed_percent_humidity = -1
    while True:
        ####logger.info('Turning ON Sensor...')
        GPIO.output(SENSOR_VCC, TURN_ON_SENSOR)

        time.sleep(1)  # Wait to get a humidity value

        ####logger.info('Turning OFF Sensor...\n')
        GPIO.output(SENSOR_VCC, TURN_OFF_SENSOR)
        new_percent_humidity = get_humidity_percent(new_humidity)
        if printed_percent_humidity != new_percent_humidity:
            printed_percent_humidity = new_percent_humidity
            logger.info('%s: Humedad = %.1f %%', time.strftime(
                "%d/%m/%y %H:%M:%S"), new_percent_humidity)
            ####logger.info('Humedad = %d\n', new_humidity)

        # Wait to get a new humidity value
        time.sleep(30)

except KeyboardInterrupt:
    logger.info('Closing program (Keyboard Interrupt)...')

except:
    logger.info('Unexpected ERROR...')

finally:
    GPIO.cleanup()
