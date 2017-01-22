import pkgutil
import wave
from datetime import datetime

from httplib2 import Http
import json
import base64
from pyaudio import PyAudio, paInt16
import encodings
import sys
import numpy as np
class Voice2Text:
    voiceAPIKEY = "UqGiNk3ymn2boGNmAnFgKXRL"
    voiceSecretKey = "320a87ae33e9ec36fe090423646a11b0"

    @staticmethod
    def get_token():
        http = Http()
        url = 'https://openapi.baidu.com/oauth/2.0/token?grant_type=client_credentials&client_id={0}&&client_secret={1}'.format(
            Voice2Text.voiceAPIKEY, Voice2Text.voiceSecretKey)
        headers = {'Content-type': 'application/json; charset=utf-8'}
        response, content = http.request(url, "GET", headers=headers)
        str = content.decode("utf-8")
        jsonData = json.loads(str)
        if (jsonData.get("error", None) is not None):
            return ""
        return jsonData.get("access_token", "")

    @staticmethod
    def get_text(token=None, buffer=bytes):
        size=len(buffer)
        base64str=base64.b64encode(buffer).decode()
        if token is None:
            return {"err_msg": "get token error"}
        http = Http()
        url = "http://vop.baidu.com/server_api"
        body = {
            "format": "wav",
            "rate": SAMPLING_RATE,
            "channel": "1",
            "token": token,
            "cuid": "B8-27-EB-87-BE-F0",
            "len": size,
            "speech": base64str,
            "lan":"zh"
        }
        headers = {'Content-type': 'audio/wav;rate='+str(SAMPLING_RATE),}
        response, content = http.request(url, "POST", headers=headers, body=json.dumps(body))
        b = content.decode("utf-8")
        jsonData = json.loads(b)
        return jsonData

    @staticmethod
    def voice2text(buffer=bytes):
        token = Voice2Text.get_token()
        result = {"err_msg": "get token error"}
        try:
            result = Voice2Text.get_text(token,buffer)
        except Exception as e:
            print(e)
        return result


NUM_SAMPLES = 2000
SAMPLING_RATE = 16000
CHANNELS = 1
SAVE_LENGTH = 2
# record time
TIME = 8

LEVEL=1500
class VoiceRecorder:
    __voiceBuffer = bytearray()

    @staticmethod
    def start():
        if (VoiceRecorder.__isWorking):
            return
        VoiceRecorder.__isWorking = True

        # open the input of wave
        pa = PyAudio()
        stream = pa.open(format=paInt16, channels=CHANNELS,
                         rate=SAMPLING_RATE, input=True,
                         frames_per_buffer=NUM_SAMPLES)
        save_buffer = []

        count = 0
        while count < TIME * 3:
            # read NUM_SAMPLES sampling data
            audioBytes = stream.read(NUM_SAMPLES)
            audio_data = np.fromstring(audioBytes, dtype=np.short)
            large_sample_count = np.sum(audio_data > LEVEL)
            save_buffer.append(audioBytes)

            count += 1
            print("---")
        VoiceRecorder.__isWorking = False
        #filename = datetime.now().strftime("%Y-%m-%d_%H_%M_%S") + ".wav"
        #VoiceRecorder.save_wave_file(filename, bytes().join(save_buffer))
        VoiceRecorder.__voiceBuffer = bytes().join(save_buffer)

        return bytes().join(save_buffer)
        # print(filename, "saved")

    @staticmethod
    def get_voice():
        return VoiceRecorder.__voiceBuffer

    @staticmethod
    def save_wave_file(filename, data):
        '''save the date to the wav file'''
        wf = wave.open(filename, 'wb')
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(SAVE_LENGTH)
        wf.setframerate(SAMPLING_RATE)
        wf.writeframes(data)
        wf.close()

    @staticmethod
    def get_voiceText():
        buffer= VoiceRecorder.start_speech()
        result=Voice2Text.voice2text(buffer)
        print(result)