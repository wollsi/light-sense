import ujson
import utime
import machine
import network
import urequests

def connectWifi():
    sta_if = network.WLAN(network.STA_IF)
    if not sta_if.isconnected():
        sta_if.active(True)
        sta_if.connect(wifi_ssid, wifi_password)
        while not sta_if.isconnected():
            pass

def __updateConfig(config_url):
    connectWifi()

    headers = {'Accept' : 'application/json'}
    response = urequests.get(config_url, headers=headers)
    print(response.content.decode('utf-8'))

    new_config = ujson.loads(response.content.decode('utf-8'))

    with open("config.json") as __f:
        local_config = ujson.load(__f)
        __f.close()

    local_config["sleep_time"] = new_config["sleep_time"]
    local_config["operation_time"] = new_config["operation_time"]

    with open("config.json", 'w') as __f:
        __f.write(ujson.dumps(local_config))


def __calculate_cycles(operation_time, sleep_time):
    if (operation_time <= 0):
        operation_time  = 1000
    if (sleep_time <= 0):
        sleep_time = 1000
    if (operation_time < sleep_time):
        operation_cycles = 1
    else:
        operation_cycles = int(operation_time/sleep_time)

    return operation_time, sleep_time, operation_cycles

def __initiate_operation(op_cycles):
    with open('cycles', 'w') as opf:
        opf.write('%d' % (op_cycles))
        opf.close()


with open("config.json") as __f:
    __data = ujson.load(__f)
    __f.close()

wifi_ssid = __data["wifi"]["ssid"]
wifi_password = __data["wifi"]["passwd"]

rest_data_url = __data["rest"]["url"]
rest_config_url = __data["rest"]["config"]

operation_time, sleep_time, operation_cycles = __calculate_cycles(__data["operation_time"], __data["sleep_time"])

if __name__ == '__main__':
    print('reset cause: ', machine.reset_cause())

    if (machine.reset_cause() == machine.HARD_RESET or machine.reset_cause() == machine.PWRON_RESET):
        print('start operating')
        print('freezing for 2 seconds')
        machine.lightsleep(2000)

        __updateConfig(rest_config_url)

        __initiate_operation(operation_cycles)
