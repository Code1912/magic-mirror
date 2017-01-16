from __future__ import print_function
import time
import sensor
import RPi.GPIO as gpio
import time

if __name__ == '__main__':

    i = 0
    # pi = pigpio.pi()
    #  s = dht11.dht11(pi, 12);
    sensor.Sensor.setup()
   # s = sensor.TemperatureSensor(4)
   # s.start()
    gpio.VERBOSE=True
    relay = sensor.Relay(18);
    while True:
        time.sleep(5)
        if i % 2 is 0:
            print("\nOPEN")
            relay.open()
        else:
            print("\nCLOSE")
            relay.close()
        i += 1

        # s.trigger()
        # print("{} {} {} {:3.2f} {} {} {} {}".format(
        ##    i, s.humidity(), s.temperature(), s.staleness(),
        #    s.bad_checksum(), s.short_message(), s.missing_message(),
        #    s.sensor_resets()))

        # s.cancel()
