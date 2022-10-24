from apscheduler.schedulers.background import BackgroundScheduler
from db.db_init import *
import requests
import time
from datetime import datetime


def weather_job():
    now_hour = datetime.now().strftime('%H:%M:%S')
    url = 'https://v0.yiketianqi.com/free/day?appid=87429221&appsecret=QjAr57VK&cityid=101050101&unescape=1'

    # noinspection PyBroadException
    try:
        response = requests.get(url)
        ret = response.json()
        today = ret['date']
        city = ret['city']
        hour = now_hour
        temp = ret['tem']
        temp_day = ret['tem_day']
        temp_night = ret['tem_night']
        condition = ret['wea_img']  # xue、lei、shachen、wu、bingbao、yun、yu、yin、qing
        win_direction = ret['win']
        win_speed = ret['win_speed']
        air = ret['air']
        humidity = ret['humidity']

        insert_data = (
            today, city, hour, temp, temp_day, temp_night, condition, win_direction, win_speed, air, humidity)

        db = connect_db()
        db.execute(
            '''INSERT OR REPLACE INTO Weather(
            weather_date,
            weather_city,
            weather_hour,
            weather_temperature,
            weather_temperature_day,
            weather_temperature_night,
            weather_condition,
            weather_win_direction,
            weather_win_speed,
            weather_air,
            weather_humidity) VALUES (?,?,?,?,?,?,?,?,?,?,?)''',
            insert_data)
        db.commit()
        print(insert_data)
    except Exception:
        pass


def start_weather_task():
    scheduler = BackgroundScheduler(timezone='Asia/Shanghai')
    scheduler.add_job(weather_job, 'cron', hour='8-22')
    scheduler.start()


if __name__ == '__main__':

    start_weather_task()

    while True:
        time.sleep(10)
