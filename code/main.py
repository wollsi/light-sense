import machine
from machine import Pin
import utime
import urequests
import network
import boot as config

OPERATING = 1
FINISHED = 0

def connectWifi():
    sta_if = network.WLAN(network.STA_IF)
    if not sta_if.isconnected():
        sta_if.active(True)
        sta_if.connect(config.wifi_ssid, config.wifi_password)
        while not sta_if.isconnected():
            pass

def check_operation_state():
    with open('cycles', 'r') as opf:
        op_cylces = int(opf.read())
        opf.close()
    if op_cylces <= 0:
        return FINISHED
    else:
        print('cycles to go: ', op_cylces-1)
        with open('cycles', 'w') as opf:
            opf.write('%d' % (op_cylces-1))
            opf.close()
        return OPERATING

def handle(old_value, new_value):
    print('Measured value: ', new_value)
    if (new_value != old_value):
        with open('data', 'w') as df:
            df.write('%d' % (new_value))
            df.close()

        connectWifi()

        data = b'%d' % new_value
        urequests.post(config.rest_data_url, data=data)


def main():
    op_state = check_operation_state()

    if op_state == OPERATING: 
        f = open('data', 'r')
        val = int(f.read())
        f.close()

        p = Pin(14, Pin.IN)
        new_value = p.value()

        handle(val, new_value)

        machine.deepsleep(config.sleep_time)

    if op_state == FINISHED:
        print('no more cycles, shuting down')

if __name__ == '__main__':
    main()

