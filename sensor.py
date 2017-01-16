from __future__ import print_function
from __future__ import print_function
from  time import sleep
import threading
import RPi.GPIO as gpio;
import Queue
import datetime
import sys
import signal
import RPi;

class Sensor:
    __registered = False

    def __init__(self):
        return

    @staticmethod
    def setup():
        gpio.setwarnings(False)
        gpio.setmode(gpio.BCM)
        if not Sensor.__registered:
            signal.signal(signal.SIGINT, Sensor.handler)
        Sensor.__registered = True
        sleep(1)

    @staticmethod
    def handler(signal_num, frame):
        print("\nPressed CTRL+C")
        gpio.cleanup()
        sys.exit(signal_num)

    @staticmethod
    def cancel():
        gpio.cleanup()


class TemperatureSensor(Sensor):
    def __init__(self, pin_num=4):
        self.pin_num = pin_num
        self.is_working = False
        self.readData = []
        self.collectDataQueue = Queue.Queue()
        self.mutex = threading.Lock()
        self.__deled = False

    def __collect_data(self):

        sleep(1)
        gpio.setup(self.pin_num, gpio.OUT)

        gpio.output(self.pin_num, gpio.LOW)
        sleep(0.02)
        gpio.output(self.pin_num, gpio.HIGH)

        gpio.setup(self.pin_num, gpio.IN)
        # test   working
        # print("sensor is working now")

        while gpio.input(self.pin_num) == gpio.HIGH:
            continue
        while gpio.input(self.pin_num) == gpio.LOW:
            continue
        while gpio.input(self.pin_num) == gpio.HIGH:
            continue
        j = 0
        data = []
        while j < 40:
            k = 0
            while gpio.input(self.pin_num) == gpio.LOW:
                continue

            while gpio.input(self.pin_num) == gpio.HIGH:
                k += 1
                if k > 100:
                    break

            if k < 10:
                data.append(0)
            else:
                data.append(1)

            j += 1

        self.collectDataQueue.put(data)

    def start(self):
        # open device
        self.is_working = True
        collection_thread = threading.Thread(target=self.__monitor)
        collection_thread.setDaemon(True)
        collection_thread.start()

        calculate_thread = threading.Thread(target=self.__calculate)
        calculate_thread.setDaemon(True)
        calculate_thread.start()

    def end(self):
        self.is_working = False

    def __monitor(self):
        while self.is_working:
            self.__collect_data()

    def __get_average(self, count):
        array_len = len(self.readData)
        if array_len == 0:
            return None

        calculate_count = count
        temp = -1
        wet = -1
        if array_len <= count:
            calculate_count = array_len
        i = 0
        while i < calculate_count and (array_len - 1 - i) > -1:
            item = self.readData[array_len - 1 - i]
            temp += item.temperature
            wet += item.wet
            i += 1
        temp /= calculate_count
        wet /= calculate_count
        return DHT11Data(temp, wet)

    def __del__(self):

        return

    @property
    def dht11_data(self):
        self.mutex.acquire()

        count = len(self.readData)
        item = None
        if count > 0:
            item = self.readData[count - 1]

        self.mutex.release()
        return item

    def __calculate(self):
        while self.is_working:
            try:
                if self.collectDataQueue.empty():
                    sleep(1)
                    continue
                # print ("queue size:",self.collectDataQueue.qsize())
                data = self.collectDataQueue.get()
                # print("data  : ",data)
                # print(len(data))
                # get temperature
                humidity_bit = data[0:8]
                humidity_point_bit = data[8:16]
                temperature_bit = data[16:24]
                temperature_point_bit = data[24:32]
                check_bit = data[32:40]

                humidity = 0
                humidity_point = 0
                temperature = 0
                temperature_point = 0
                check = 0

                for i in range(8):
                    humidity += humidity_bit[i] * 2 ** (7 - i)
                    humidity_point += humidity_point_bit[i] * 2 ** (7 - i)
                    temperature += temperature_bit[i] * 2 ** (7 - i)
                    temperature_point += temperature_point_bit[i] * 2 ** (7 - i)
                    check += check_bit[i] * 2 ** (7 - i)

                tmp = humidity + humidity_point + temperature + temperature_point

                if check == tmp:
                    print("temperature : ", temperature, "wet : ", humidity)
                    self.mutex.acquire()
                    array_len = len(self.readData)
                    # remove over length data
                    if array_len > 100:
                        for i in range(0, array_len - 100 - 1):
                            self.readData.pop(i)
                    average = self.__get_average(10)
                    if (average is None):
                        self.mutex.release()
                        self.readData.append(DHT11Data(temperature, humidity))
                        continue

                    valid_rang = 0.3
                    temp_valid = average.temperature * (1 - valid_rang) < temperature < average.temperature * (
                        1 + valid_rang)
                    wet_valid = average.wet * (1 - valid_rang) < humidity < average.wet * (1 + valid_rang)
                    if temp_valid and wet_valid:
                        self.readData.append(DHT11Data(temperature, humidity))
                    self.mutex.release()
                    # else:
                    # print("wrong")
                    # print("temperature : ", temperature, ", humidity : ", humidity, " check : ", check, " tmp : ", tmp)
            except Exception as e:
                print("---- calculate error----", e)
                continue

    def __del__(self):
        self.__deled = True


class DHT11Data:
    def __init__(self, temp, wet):

        self._temperature = temp
        self._wet = wet

    @property
    def temperature(self):
        return self._temperature

    @temperature.setter  # res
    def temperature(self, value):
        if not isinstance(value, int):
            raise ValueError('temperature must be an integer!')
        self._temperature = value

    @property
    def wet(self):
        return self._wet

    @wet.setter
    def wet(self, value):
        if not isinstance(value, int):
            raise ValueError('wet must be an integer!')
        self._wet = value


class Relay(Sensor):
    def __init__(self, pin_num=18):
        self.pin_num = pin_num
        gpio.setup(self.pin_num, gpio.OUT,initial=gpio.HIGH)
        self.close()
        return

    def open(self):
        gpio.setup(self.pin_num, gpio.LOW)
        sleep(0.02)
        return

    def close(self):
        gpio.setup(self.pin_num, gpio.HIGH)
        sleep(0.02)
        return

    def __del__(self):
        return
