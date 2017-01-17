/**
 * Created by Code1912 on 2017/1/16.
 */
(function (window) {
    let onFail = function (e) {
        console.log('Rejected!', e);
    };
    let timer = null;
    let isWorking = false;
    let onSuccess = function (s) {
        let context = new AudioContext();
        context.sampleRate=8000;
        let mediaStreamSource = context.createMediaStreamSource(s);
        console.log(mediaStreamSource)
        recorder = new Recorder(mediaStreamSource);
        recorder.record();

        // audio loopback
        // mediaStreamSource.connect(context.destination);
    };

    window.URL = window.URL || window.webkitURL;
    navigator.getUserMedia = navigator.getUserMedia || navigator.webkitGetUserMedia || navigator.mozGetUserMedia || navigator.msGetUserMedia;

    let recorder;
    //let audio = document.querySelector('audio');

    function startRecording() {
        if (navigator.getUserMedia) {
            navigator.getUserMedia({audio: true}, onSuccess, onFail);
        } else {
            console.log('navigator.getUserMedia not present');
        }
    }

    function stopRecording() {
        timer && clearTimeout(timer);
        timer = null;
        isWorking = false;
        recorder.stop();
    }

    let startSpeech = function () {
        if (isWorking)
            return
        isWorking = true;
        startRecording();
        timer = setTimeout(function () {
            stopRecording();
        }, 1000 * 10);
    };
    let getVoiceData = function () {
        stopRecording();
        return new Promise(function (resolve, reject) {
            try {
                recorder.exportWAV(function (s) {
                    console.log(s);
                    resolve(s);
                });
            }
            catch (e) {
                console.log("export voice error", s);
                reject(false);
            }
        });
    };
    window.startSpeech = startSpeech;
    window.getVoiceData = getVoiceData;
})(window);