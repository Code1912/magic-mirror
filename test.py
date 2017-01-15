from __future__ import print_function
import time
import sensor

if __name__ == '__main__':

    i = 0
    # pi = pigpio.pi()
    #  s = dht11.dht11(pi, 12);
    s = sensor.TemperatureSensor(4)
    s.start()
    while True:
        time.sleep(1)
        item = s.dht11_data;
        if(item.temperature==-1):
            continue
        print("temperature:", item.temperature, "wet :", item.wet,"---------")
        i += 1
        # s.trigger()
        # print("{} {} {} {:3.2f} {} {} {} {}".format(
        ##    i, s.humidity(), s.temperature(), s.staleness(),
        #    s.bad_checksum(), s.short_message(), s.missing_message(),
        #    s.sensor_resets()))

        # s.cancel()
