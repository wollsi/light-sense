import machine
from machine import Pin
from machine import deepsleep
import utime
import boot as config

val = 0

def handle(p):
    global val
    new_value = p.value()
    print('Measured value: ', new_value)
    if (new_value != val):
        f = open('data.txt', 'w')
        f.write('%d\n' % (new_value))
        f.close()
        print('\told value ', val)
        print('\tnew value', new_value)
        val = new_value
        utime.sleep_ms(500)

if machine.reset_cause() == machine.DEEPSLEEP_RESET:
    print('woke from a deep sleep')

    f = open('data.txt', 'r')
    val = int(f.read())
    print('Read: ', val)
    f.close()

    p = Pin(14, Pin.IN)
    handle(p)
else:
    print('power on or hard reset')
    print('freezing for 5 seconds')
    utime.sleep(5)


def deep_sleep(msecs):
    # configure RTC.ALARM0 to be able to wake the device
    rtc = machine.RTC()
    rtc.irq(trigger=rtc.ALARM0, wake=machine.DEEPSLEEP)

    rtc.alarm(rtc.ALARM0, msecs)

    # put the device to sleep
    print("Sleeping now")
    machine.deepsleep()

deep_sleep(config.sleep_time)