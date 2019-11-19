Pyrduino
========

What is pyrduino?
-----------------

Pyrduino is a wrapper around pyfirmata package which aims to ease and do programming on Arduino board more Pythonic
and object ordiented way.

Prerequisites
-------------

What you need:
  * Arduino board (obviously)
  * Arduino IDE (for uploading StandardFirmata into the board https://www.arduino.cc/en/main/software)
  * Currently I am sticking on Python 3.x as a  requirement, since everyone should be using that
  instead of Python 2 anyways
  

How to use?
-----------

**First of all I suggest always to use virtualenv and never do any project work without it**
https://virtualenv.pypa.io/en/latest/

**My dearest suggestion is to use virtualenvwrapper**
https://virtualenvwrapper.readthedocs.io/en/latest/


Now onto the business...

There is a example package bundled with the pyrduino wrapper and the installation script at least tries to install it
(Jump to [It's not working]('#not_working') section if you head into problems):

`pip install -e .`

This will install a `pyrduino_example` command line script for you. Just run it to see the commands it provides.
It also is depended on click package (https://click.palletsprojects.com/en/7.x/),
which is **NOT** included in the setup requirements because the actual
pyrduino doesn't need it, so you need to install it ourself if needed: `pip install click`.

The basic usage of the wrapper should be quite clear just by looking at the examples. But let's see what we get...

Features
--------
* Initialize a board to a real Python object instance by device id and device type
* Register pins by name to different modes (input/output, analog/digital/servo/pwm) (as an array is also supported)
* Read/write from the pins by their names and pass time on board
* Fetch registered pins by type or mode
* Remembers the last used pin by name for convenience


A simple example
----------------

```python
from pyrduino import *
# Let's create a board instance or our Pyrduino wrapper
board = Pyrduino(board_id='/dev/ttyUSB0', board_type=BOARD_TYPE_ARDUINO_MEGA)
# Let's register pind 13 to digital output with name 'light'
board.register_pin(name='light', number=13, pin_type=PIN_TYPE_DIGITAL, pin_mode=PIN_MODE_OUTPUT)
led_on = 1  # Let's use integer instead of boolean, so we can write this directly to the named pin
# Let's blink the led on our named pin 'light'
for x in range(100):
    if led_on == 1:
        led_on = 0
    else:
        led_on = 1
        
    # The wrapper instance will actually remember that we used the name 'light', so it could be 
    # omitted on later iterations, but let's go this way. First call or read/write should always include the name
    board.write_pin(name='light', value=led_on)
    board.pass_time(0.05)  # Sleep for a bit
    
board.exit_board()  # Not actually needed, since this is called in the destructor

```

Why?
----

I tend to think that this is somewhat more Pythonic way of dealing with this stuff. You just register the pins by name and work
with them by their names and you only have to worry about that configuration in the initialization phase and then
just forget about the config part and start programming with the logical stuff in more human readable way and
more Pythonic and object oriented way. Basically it is just a higher level abstraction of the things to do with
the board, but I think that this simplifies things quite a lot and makes it more confortable to do the actual
programming.

<a id="not_working"></a>It's not working?!!
-------------------

I know, my setup.py is somehow not right now and you need to use `pip install -r requirements.txt` to get the packages 
right. Mabe someone could help me? If so, please, contact me. It's my very first time to deal with setuptools since
I have never had the need for packaging anything and have always used pip and requirements.txt. But that click
package is not in requirements.txt, since it's not needed by the wrapper, but only for the examples. It's a great package
though! I'll link it again :) (https://click.palletsprojects.com/en/7.x/)

It's still not working?!
------------------------

Remember always to use Arduino IDE to push StandardFirmata into the board. pyfirmata **WILL NOT** work without that.

And yes, I have made that mistake too. Uploaded some other stuff, and then wondering why isn't my lovely wrapper working?
Solution: Always remember to upload StandardFirmata before working with pyfirmata or pyrduino.

For other problems with this package you can always contact me.


TODO
----

Whatever comes to mind?! Please give/send feedback and suggestions into my email: <mailto:ahti.komu@gmail.com>
