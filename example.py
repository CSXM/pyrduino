# -*- coding: utf-8 -*-
# NOTE: This example requires click package: https://click.palletsprojects.com/en/7.x/

import logging
import click

logger = logging.getLogger('Pyrduino test')

# Import stuff from our pyrduino package
from pyrduino.pyrduino import *
# Import morse code for our example code
from morse_code import morseAlphabet

class OurProgram:
    BLINK_TYPE_SEQUENTICAL = 'sequentical'
    BLINK_TYPE_CONCURRENT = 'concurrent'

    def __init__(self, board_id, board_type):
        """ Constructor of the program

        :param board_id: Id of the board. In Windows, usually 'COM3' or similar
        :type board_id: str
        :param board_type: Type of the board. One of the constant values defined in the beginning of this file.
        :type board_type: str
        """
        # Let's assume that the board can't be created and declare a None instance
        self.board = None
        try:
            logger.debug('Trying to register board')
            self.board = Pyrduino(board_id=board_id, board_type=board_type)
            logger.debug('Board registered')
        except Exception as e:
            error_msg = 'Could not create a board with these values: {} {}, error: {}'.format(board_id, board_type, e)
            logger.error(error_msg)

    def do_something(self):
        """ Method that does some simple stuff with the board. Comments explain this stuff.

        This is just an example of doing some things.

        :return: A list of results from the read pin
        :rtype: list
        """
        if not self.board:
            # If we didn't create a board successfully, let's just return to go away
            # Also we will return something else to print instead of the list of results
            return "Sorry, Couldn't create board"
        # Register some pins
        self.board.register_pin(name='write pin', number=1, pin_type=PIN_TYPE_DIGITAL, pin_mode=PIN_MODE_OUTPUT)
        self.board.register_pin(name='read pin', number=13, pin_type=PIN_TYPE_ANALOG, pin_mode=PIN_MODE_INPUT)
        # Initialize a list for results from the reading pin
        our_list = list()
        # We will loop values from 0 - 9 whith this (range takes a maximum number of values and starts from 0)
        for x in range(10):
            # Let's write a value of x + 1 to the write pin (range starts from 0, we want to add 1 to that
            self.board.write_pin(name='write pin', value=x+1)
            time.sleep(2)  # Let's wait for 2 seconds before reading the value from another pin
            # Let's read the read pin value and add it to our list
            our_list.append(self.board.read_pin('read pin'))

        # Finally let's return our results
        return our_list

    def blink_light(self, amount=100):
        """ Blinks a led for amount of times on pin 13

        :param amount: Amount of times to blink
        :type amount: int
        :return: Nothing
        """
        self.board.register_pin(name='light', number=13, pin_type=PIN_TYPE_DIGITAL, pin_mode=PIN_MODE_OUTPUT)
        led_on = 1
        for x in range(amount):
            if led_on == 1:
                led_on = 0
            else:
                led_on = 1
            self.board.write_pin(name='light', value=led_on)
            self.board.pass_time(0.05)
        self.board.write_pin(name='light', value=0)

    def smooth_piezo(self):
        """ Writes values from 1 to 1000 to a piezo in pin 9 at 0.01 second intervals

        :return: Nothing
        """
        self.board.register_pin(name='piezo', number=9, pin_type=PIN_TYPE_DIGITAL, pin_mode=PIN_MODE_PWM)

        for v in range(1, 1000):
           self.board.write_pin(value=float(v)/1000)
           self.board.pass_time(0.01)
        self.board.write_pin(value=0)

    def morse(self, text='SOS', speed_factor=6):
        """ Does a morse code

        :param text: Text to morse
        :type text: str
        :param speed_factor: Speed factor, the higher the value, the faster the morse
        :type speed_factor: int
        :return: Nothing
        """
        text = text.upper()
        characters = list(text)
        beep_list = list()
        for character in characters:
            morse_characters = morseAlphabet[character]
            for morse_character in morse_characters:
                if morse_character == ".":
                    beep_list.append(1)
                else:
                    beep_list.append(3)
        self.board.register_pin(name='beep', number=9, pin_type=PIN_TYPE_DIGITAL, pin_mode=PIN_MODE_PWM)
        self.board.register_pin(name='light', number=13, pin_type=PIN_TYPE_DIGITAL, pin_mode=PIN_MODE_OUTPUT)
        self.board.write_pin(name='beep', value=0)
        logger.debug('starting to morse')
        for beep in beep_list:
            self.board.write_pin(name='light', value=1)
            self.board.write_pin(name='beep', value=0.6)
            self.board.pass_time(beep/speed_factor)
            self.board.write_pin(name='light', value=0)
            self.board.write_pin(name='beep', value=0)
            self.board.pass_time(0.1)

    def test_piezo(self):
        """ Tests that piezo is working on pin 9 by writing a value of 0.9 for 1 second

        :return: Nothing
        """
        self.board.register_pin(name='beep', number=9, pin_type=PIN_TYPE_DIGITAL, pin_mode=PIN_MODE_PWM)
        self.board.write_pin(value=0.9)
        self.board.pass_time(1)
        self.board.write_pin(value=0)

    def beep_with_button(self, sound_level=0.9):
        self.board.register_pin(name='button', number=12, pin_type=PIN_TYPE_DIGITAL, pin_mode=PIN_MODE_INPUT)
        self.board.register_pin(name='beep', number=9, pin_type=PIN_TYPE_DIGITAL, pin_mode=PIN_MODE_PWM)
        sounding = False
        # Shut down the piezo at the start
        self.board.write_pin(name='beep', value=0)
        while True:
            # Get the button pressed status
            button_pressed = self.board.read_pin(name='button')
            if not sounding and button_pressed:
                self.board.write_pin(name='beep', value=sound_level)
                sounding = True
            elif sounding and not button_pressed:
                self.board.write_pin(name='beep', value=0)
                sounding = False

            self.board.pass_time(0.05)

    def blink_with_input(self, min_pin=11, max_pin=13, blink_type=BLINK_TYPE_SEQUENTICAL, interval=0.2, amount=10):
        self.board.register_pin_array(min_pin=min_pin, max_pin=max_pin)
        for occurrence in range(amount):
            if blink_type == self.BLINK_TYPE_SEQUENTICAL:
                for pin_no in range(min_pin, max_pin + 1):
                    self.board.write_pin(name=str(pin_no), value=1)
                    self.board.pass_time(interval)
                for pin_no in range(min_pin, max_pin + 1):
                    self.board.write_pin(name=str(pin_no), value=0)
                    self.board.pass_time(interval)
            else:
                for pin_no in range(min_pin, max_pin +1):
                    self.board.write_pin(name=str(pin_no), value=1)
                self.board.pass_time(interval)
                for pin_no in range(min_pin, max_pin + 1):
                    self.board.write_pin(name=str(pin_no), value=0)
                self.board.pass_time(interval)



    def __del__(self):
        """ Destructor which will also call the exit_board method of the board

        :return: None
        """
        # Only call exit_board if we had a successfully created board
        if self.board:
            self.board.exit_board()
        # We could also do "del self.board" which would do the same thing.


# Let's create an user interface for our example stuff (Requires click package)

@click.group()
@click.option('-i', '--board_id', default='/dev/ttyUSB0', show_default=True,
              help='Board ID, typically a tty or USB port')
@click.option('-t', '--board_type', default=BOARD_TYPE_ARDUINO_MEGA, show_default=True,
              help='Board type from pyrduino choices')
@click.pass_context
def cli(ctx, board_id, board_type):
    ctx.obj = OurProgram(board_id=board_id, board_type=board_type)


@cli.command()
@click.pass_obj
def piezo_test(our_example):
    """ Tests piezo from board pin 9

    \f
    :param our_example: Passed instance of OurProgram
    :return: Nothing
    """
    our_example.test_piezo()


@cli.command()
@click.pass_obj
def beep_with_button(our_example):
    """ Beeps the piezo in pin 9 when button is pressed in pin 12

    This will exit with Ctrl+D

    \f
    :param our_example: Passed instance of OurProgram
    :return: Nothing
    """
    our_example.beep_with_button()


@cli.command()
@click.pass_obj
def smooth_piezo(our_example):
    """Does a 'smooth' piezo

    \f
    :param our_example: Passed instance of OurProgram
    :return: Nothing
    """
    our_example.smooth_piezo()


@cli.command()
@click.pass_obj
@click.argument('text', type=str)
@click.argument('speed_factor', required=False, type=int)
def morse(our_example, text, speed_factor):
    """ Does a morse code with TEXT and optional SPEED.

        Piezo should be on pin 9 and a led on pin 13.

    \f
    :param our_example: Passed instance of OurProgram
    :param text: Text to morse
    :type text: str
    :param speed_factor: Speed for the morse
    :type speed_factor: int
    :return: Nothing
    """
    if not speed_factor:
        our_example.morse(text=text)
    else:
        our_example.morse(text=text, speed_factor=speed_factor)


@cli.command()
@click.pass_obj
def blink(our_example):
    """Blinks a led a hundred times on pin 13

    \f
    :param our_example: Passed instance of OurProgram
    :return: Nothing
    """
    our_example.blink_light()


@cli.command()
@click.pass_obj
@click.argument('amount', type=int)
def blink_x(our_example, amount):
    """ Blinks a lef AMOUNT of times on pin 13

    \f
    :param our_example: Passed instance of OurProgram
    :param amount: Amount of times to blink the led
    :type amount: int
    :return: Nothing
    """
    our_example.blink_light(amount=amount)


@cli.command()
@click.pass_obj
@click.option('--min-pin', help='Minimum pin', default=11, type=int)
@click.option('--max-pin', help='Maximum pin', default=13, type=int)
@click.argument('blink_type', default=OurProgram.BLINK_TYPE_SEQUENTICAL, required=False)
@click.argument('interval', default=0.2, type=float, required=False)
@click.argument('amount', default=10, type=int, required=False)
def blink_with_input(our_example, min_pin, max_pin, blink_type, interval, amount):
    """ Blink leds with some input examples

    \f
    :param our_example: Passed instance of OurProgram
    :param min_pin: Pin number of the lowest pin
    :type min_pin: int
    :param max_pin: Pin number of the highest pin
    :type max_pin: int
    :param blink_type: Blink type. Either 'concurrent' or 'sequentical'
    :type blink_type: str
    :param interval: The time of seconds to sleep between the events
    :type interval: float
    :param amount: Amount of 'rounds' to go
    :type amount: int
    :return: Nothing
    """
    our_example.blink_with_input(min_pin=min_pin, max_pin=max_pin, blink_type=blink_type,
                                 interval=interval, amount=amount)
