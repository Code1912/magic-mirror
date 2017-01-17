/**
 * Created by Code1912 on 2017/1/16.
 */
(function () {
    let app = angular.module('mirror', []);
    app.controller("appCtrl", function ($scope, $timeout, $interval, $http) {
        let apiKey = "329f1a4b88eb176c4afe88abb913cb7c";
        let config = {city: {cityName: "成都", cityId: "101270101"}}
        $scope.date = moment().format('YYYY年MM月DD日  ');
        $scope.time = moment().format('HH:MM:ss');
        $scope.startSpeech = () => {
            startSpeech()
        };
        $scope.endSpeech = () => {
            getVoiceData().then(blob => {
                let token = "";
                let audio = document.querySelector('audio');
                audio.src = window.URL.createObjectURL(blob);
                voiceToText(blob)


            })
        };

        $scope.weatherIcon = function (str) {

        };

        function blobToBase64(blob) {
            return new Promise((resolve, rejcet) => {
                let reader = new window.FileReader();
                reader.readAsDataURL(blob);
                reader.onloadend = function () {
                    let base64data = reader.result;
                    console.log("blobTOBase64OK");
                    resolve(base64data)
                }
            })
        }

        let voiceToText = (blob) => {
            var from = new FormData(); //初始化一个FormData实例
            from.append('voice', blob);
            $http.post(`/voice2text`, from).success(res => {
                console.log(res);
            })

        };
        let refreshTime = function () {
            $scope.date = moment().format('YYYY年MM月DD日  ');
            $scope.time = moment().format('HH:MM:ss');
        };
        let getConfig = function () {
            return $http.get("/config").success(function (data) {
                if (!data) {
                    return;
                }
                let oldData = config;
                config = decode(data);
                if (oldData.city.cityName != data.city.cityName) {
                    refreshWeather();
                }
            });
        };
        let refreshWeather = function () {
            $http.get(`http://apis.baidu.com/apistore/weatherservice/recentweathers?cityname=${config.city.cityName}&cityid=${config.city.cityId}`, {
                headers: {"apikey": apiKey}
            }).success(function (data) {
                console.log(data)
            })
        };
        let decode = function (json) {
            return JSON.parse(decodeURIComponent(JSON.stringify(json)));
        };
        getConfig().then(refreshWeather);
        $interval(refreshTime, 900);
        //$interval(getConfig, 2000);
        $interval(refreshWeather, 1000 * 60 * 20);
    })
})(window);
