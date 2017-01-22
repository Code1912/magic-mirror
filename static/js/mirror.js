/**
 * Created by Code1912 on 2017/1/16.
 */
(function () {
    let app = angular.module('mirror', []);
    window.config = {city: {cityName: "成都", cityId: "101270101"}};
    window.decodeJSON = function (json) {
        return JSON.parse(decodeURIComponent(JSON.stringify(json)));
    };
    window.decodeJSONStr = function (jsonStr) {
        return JSON.parse(decodeURIComponent(jsonStr));
    };
    app.controller("appCtrl", function ($scope, $timeout, $interval, $http) {
        let apiKey = "329f1a4b88eb176c4afe88abb913cb7c";
        let getConfig = function () {
            return $http.get("/config").success(function (data) {
                if (!data) {
                    return;
                }
                let oldData = window.config;
                window.config = decodeJSON(data);
                if (oldData.city.cityName != data.city.cityName) {
                    $scope.$broadcast("weather");
                }
            });
        };
        getConfig();
        $interval(getConfig, 20000);

    });

    app.controller("timeCtrl", function ($scope, $timeout, $interval) {
        let refreshTime = function () {
            $scope.date = moment().format('YYYY年MM月DD日  ');
            $scope.time = moment().format('HH:MM:ss');
        };
        $interval(refreshTime, 900);
    });

    app.controller("weatherCtrl", function ($scope, $timeout, $interval, $http) {
        //定义天气类型
        this.weatherArr = {
            "00": "晴",
            "01": "多云",
            "02": "阴",
            "03": "阵雨",
            "04": "雷阵雨",
            "05": "雷阵雨伴有冰雹",
            "06": "雨夹雪",
            "07": "小雨",
            "08": "中雨",
            "09": "大雨",
            "10": "暴雨",
            "11": "大暴雨",
            "12": "特大暴雨",
            "13": "阵雪",
            "14": "小雪",
            "15": "中雪",
            "16": "大雪",
            "17": "暴雪",
            "18": "雾",
            "19": "冻雨",
            "20": "沙尘暴",
            "21": "小到中雨",
            "22": "中到大雨",
            "23": "大到暴雨",
            "24": "暴雨到大暴雨",
            "25": "大暴雨到特大暴雨",
            "26": "小到中雪",
            "27": "中到大雪",
            "28": "大到暴雪",
            "29": "浮尘",
            "30": "扬沙",
            "31": "强沙尘暴",
            "53": "霾",
            "99": ""
        };
        //定义风向数组
        this.fxArr = {
            "0": "无持续风向",
            "1": "东北风",
            "2": "东风",
            "3": "东南风",
            "4": "南风",
            "5": "西南风",
            "6": "西风",
            "7": "西北风",
            "8": "北风",
            "9": "旋转风"
        };
        //定义风力数组
        this.flArr = {
            "0": "微风",
            "1": "3-4级",
            "2": "4-5级",
            "3": "5-6级",
            "4": "6-7级",
            "5": "7-8级",
            "6": "8-9级",
            "7": "9-10级",
            "8": "10-11级",
            "9": "11-12级"
        };

        let refreshWeather = function () {
            $http.get("/weather").success(res => {
                res = decodeJSON(res);
                $scope.weatherList = res.results[0].daily;
            })
        };
        let refreshWeatherNow = function () {
            $http.get("/weather/now").success(res => {
                res = decodeJSON(res);
                $scope.weather = res.results[0].now;
            })
        };

        $scope.$on("weather", () => {
            refreshWeather();
            refreshWeatherNow();
        });
        refreshWeather();
        refreshWeatherNow();
        $interval(refreshWeather, 1000 * 60 * 20);
        $interval(refreshWeatherNow, 1000 * 60 * 20);
    });

})(window);

