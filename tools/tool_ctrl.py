from db.db_init import *


def query_holiday_state(db: sqlite3.Connection, start, end):
    real_start = '0000-00-00' if start is None else start
    real_end = '9999-99-99' if end is None else end
    db.row_factory = dict_factory

    cursor = db.execute('SELECT * FROM Holiday WHERE date >= ? AND date <= ? ORDER BY date ASC',
                        (real_start, real_end))
    return cursor.fetchall()


def query_weather(db: sqlite3.Connection, start, end):
    real_start = '0000-00-00' if start is None else start
    real_end = '9999-99-99' if end is None else end
    db.row_factory = dict_factory

    cursor = db.execute(
        'SELECT * FROM Weather WHERE weather_date >= ? AND weather_date <= ? ORDER BY weather_date, weather_hour ASC',
        (real_start, real_end))

    ret_list = []
    cur_obj = dict()

    current_date = ''
    for ele in cursor:
        ele_date = ele.get('weather_date')
        if ele_date != current_date:
            current_date = ele_date
            cur_obj = dict()
            cur_obj['date'] = current_date
            cur_obj['city'] = ele.get('weather_city')
            cur_obj['hour_list'] = []

            hour_obj = dict()
            hour_obj['weather_hour'] = ele.get('weather_hour')
            hour_obj['weather_temperature'] = ele.get('weather_temperature')
            hour_obj['weather_temperature_day'] = ele.get('weather_temperature_day')
            hour_obj['weather_temperature_night'] = ele.get('weather_temperature_night')
            hour_obj['weather_condition'] = ele.get('weather_condition')
            hour_obj['weather_win_direction'] = ele.get('weather_win_direction')
            hour_obj['weather_win_speed'] = ele.get('weather_win_speed')
            hour_obj['weather_air'] = ele.get('weather_air')
            hour_obj['weather_humidity'] = ele.get('weather_humidity')

            cur_obj['hour_list'].append(hour_obj)
            ret_list.append(cur_obj)
        else:
            hour_obj = dict()
            hour_obj['weather_hour'] = ele.get('weather_hour')
            hour_obj['weather_temperature'] = ele.get('weather_temperature')
            hour_obj['weather_temperature_day'] = ele.get('weather_temperature_day')
            hour_obj['weather_temperature_night'] = ele.get('weather_temperature_night')
            hour_obj['weather_condition'] = ele.get('weather_condition')
            hour_obj['weather_win_direction'] = ele.get('weather_win_direction')
            hour_obj['weather_win_speed'] = ele.get('weather_win_speed')
            hour_obj['weather_air'] = ele.get('weather_air')
            hour_obj['weather_humidity'] = ele.get('weather_humidity')

            cur_obj['hour_list'].append(hour_obj)

        print(ele)
    return ret_list
