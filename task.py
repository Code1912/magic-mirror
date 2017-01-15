import webbrowser
import threading
import platform
import time
import sensor


class Task:
    def __init__(self):
        self.__mirror_url = "http://127.0.0.1:5000"

    def start(self):
        open_browser_thread = threading.Thread(target=self.__open_browser)
        open_browser_thread.setDaemon(True)
        open_browser_thread.start()

    def __open_browser(self):
        # time.sleep(3)
        try:
            webbrowser.get(self.__getChromeUrl()).open(self.__mirror_url)
            print ("start magic mirror")
            tSensor= sensor.TemperatureSensor(4)
            tSensor.start()
        except Exception, e:
            print (Exception, ":", e)

    def __getChromeUrl(self):
        sysStr = platform.system()
        print sysStr
        if (sysStr == "Windows"):
            return "C:/Users/Code1912/AppData/Local/Google/Chrome/Application/chrome.exe --kiosk %s"
        else:
            # return "/opt/google/chrome"
            return " /usr/bin/chromium-browser --kiosk %s";
