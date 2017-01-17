#coding=utf-8
import sys
class Config:
    city={"cityName":'成都',"cityId":"101270101"}
    is_need_refresh=False

    @staticmethod
    def get_dconfig():
        return  {
            "city":Config.city,
            "is_need_refresh":Config.is_need_refresh
        }