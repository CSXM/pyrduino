# -*- coding: utf-8 -*-
import time
import logging
import sys

logger = logging.getLogger('Pyrduino')
logger.setLevel(logging.DEBUG)
logger.addHandler(logging.StreamHandler(sys.stdout))

from dotmap import DotMap
from pyfirmata import Arduino, ArduinoMega, ArduinoNano, ArduinoDue, util

BOARD_TYPE_ARDUINO = 'arduino'
BOARD_TYPE_ARDUINO_MEGA = 'mega'
BOARD_TYPE_ARDUINO_NANO = 'nano'
BOARD_TYPE_ARDUINO_DUE = 'due'
BOARD_TYPES = [
    BOARD_TYPE_ARDUINO,
    BOARD_TYPE_ARDUINO_MEGA,
    BOARD_TYPE_ARDUINO_NANO,
    BOARD_TYPE_ARDUINO_DUE
]

# These literals will actually be forming parts of the string for getting a pin from pyfirmata board instance
PIN_TYPE_ANALOG = 'a'
PIN_TYPE_DIGITAL = 'd'

PIN_MODE_INPUT = 'i'
PIN_MODE_OUTPUT = 'o'
PIN_MODE_SERVO = 's'
PIN_MODE_PWM = 'p'


class Pyrduino:
    def __init__(self, board_id, board_type=BOARD_TYPE_ARDUINO, loglevel=logging.DEBUG):
        """ Constructor for the board controller

        :param board_id: Id of the board. In Windows, usually 'COM3' or similar, in Linux usually /dev/ttyXXX
        :type board_id: str
        :param board_type: Type of the board. One of the constant values defined in the beginning of this file.
        :type board_type: str
        :param loglevel: Log level
        :type loglevel: One of the Python's logging package log levels. (Default: logging.DEBUG)
        """
        # Let's set up a lookup table to get different types of board classes from board type choices
        board_type_lookup_table = {
            BOARD_TYPE_ARDUINO: Arduino,
            BOARD_TYPE_ARDUINO_MEGA: ArduinoMega,
            BOARD_TYPE_ARDUINO_NANO: ArduinoNano,
            BOARD_TYPE_ARDUINO_DUE: ArduinoDue
        }
        # Now let us get the board type class from the lookup table and instantiate it with board id
        # This is a shortcut for if-else clauses and a shorter version of this:
        # board_class = board_type_lookup_table[board_type]
        # self.board = board_class(board_id)

        # Let's assume that the board can't be created and declare a None instance
        self.board = None
        try:
            self.board = board_type_lookup_table[board_type](board_id)
            logger.debug('Registered a board with type: {} id: {}'.format(board_type, board_id))
        except Exception as e:
            raise e

        # Give the board some time to synchronize
        time.sleep(5)

        # Let's start the iterator so the board read values can be passed to pyfirmata
        it = util.Iterator(self.board)
        it.start()

        # Dictionary for storing registered ports by name
        self.registered_pins = dict()

        self.last_pin_name = None

    def exit_board(self):
        """ Just a method for convenience to exit the board

        :return: None
        """
        # Only call exit if the board exists
        if self.board:
            self.board.exit()

    def __del__(self):
        """ Destructor which calls the exit_board method for the board

        :return: None
        """
        self.exit_board()

    def register_pin(self, name, number, pin_type=PIN_TYPE_DIGITAL, pin_mode=PIN_MODE_OUTPUT):
        """ Registers a pin ot our Pyrduino class

        :param name: Name of the pin
        :type name: str
        :param number: Number of the pin
        :type number: int
        :param pin_type: Type of the pin (digital, analog)
        :param pin_mode: Mode of the pin (input, output, servo, pwm)
        :return: None
        """
        # Let's make our pin DotMap (an enhanced version of Python dictionary)
        pin = DotMap()
        # Assign a number and a pin type and mode
        pin.number = number
        pin.pin_type = pin_type
        pin.pin_mode = pin_mode
        # Let's create the actual pin and store that too, The format is for example 'd:13:i'
        pin_string = '{}:{}:{}'.format(pin_type, str(number), pin_mode)
        logger.debug('Registering a pin with string: ' + pin_string + ' with name: ' + name)
        actual_pin = self.board.get_pin(pin_string)
        pin.pin = actual_pin
        time.sleep(1)
        # Add it to our registered pins with the desired name
        self.registered_pins[name] = pin
        self.last_pin_name = name


    def register_pin_array(self, min_pin=11, max_pin=13, pin_type=PIN_TYPE_DIGITAL, pin_mode=PIN_MODE_OUTPUT):
        """ A helper to register multiple pins at once. Refer to @register_pin method.

        :param min_pin: Pin to start with
        :type min_pin: int
        :param max_pin: The last pin to register
        :type max_pin: int
        :param pin_type: Type of the pins to register
        :param pin_mode: Mode of the pins to register
        :return: None
        """
        for x in range(min_pin, max_pin + 1):  # +1 since range will omit the last value
            # Let's register the pins by desired type with the name of being a string version of the number
            self.register_pin(name=str(x), number=x, pin_type=pin_type, pin_mode=pin_mode)

    def get_registered_pin(self, name=None):
        """ Returns a registered pin by a name

        :param name: Name of the pin
        :type name: str
        :return: Pin
        :rtype a DotMap instance
        """
        if not name:
            assert self.last_pin_name, 'You must give a pin name if pin name has not been used before'
            name = self.last_pin_name
        if name in self.registered_pins.keys():
            # Let's keep the last used pin in store, for convenience
            self.last_pin_name = name
            logger.debug('Got a pin named: ' + name)
            return self.registered_pins[name]
        else:
            raise Exception('No pin registered with that name')

    def write_pin(self, name=None, value=0):
        """ Write a value to the pin

        :param name: Name of a registered pin
        :type name: str
        :param value: Value to write
        :type value: int or float
        :return: None
        """
        self.get_registered_pin(name).pin.write(value)
        logger.debug('Writing to pin a value: ' + str(value))

    def read_pin(self, name):
        """ Read a pin value

        :param name: Name of a registered pin
        :type name: str
        :return: Pin value
        """
        read_value = self.get_registered_pin(name).pin.read()
        logger.debug('Read a value from a pin: ' + str(read_value))
        return read_value

    def pass_time(self, value):
        """ Pass a time on board

        :param value: Time to pass
        :type value: float
        :return: None
        """
        self.board.pass_time(t=value)

    # Some methods just by chance if they are ever needed:

    def get_pins_by_type(self, pin_type=PIN_TYPE_ANALOG):
        return [pin for pin in self.registered_pins.values() if pin.pin_type == pin_type]

    def get_pins_by_mode(self, pin_mode=PIN_MODE_INPUT):
        return [pin for pin in self.registered_pins.values() if pin.pin_mode == pin_mode]

