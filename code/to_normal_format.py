def to_normal_time(time: str):
    if time.endswith('PM'):
        time = [int(i) for i in time.split()[0].split(':')]
        time[0] += 12
        return f'{time[0]}:{time[1]}'
    return first_el(time)


def to_current(json):
    location = json['location']
    current = json['current']
    air_quality = current['air_quality']

    return f"""Сейчас в {location['name']}:

Местные дата и время: {location['localtime']}

{current['condition']['text']}
Температура: {current['temp_c']}C ({current['temp_f']}F)
Ощущается как {current['feelslike_c']}C ({current['feelslike_f']}F)

Влажность: {current['humidity']}%

Давление воздуза: {round(current['pressure_mb'] * 0.750064, 2)} мм рт.ст.

Скорость ветра: {current['wind_kph']} км/ч ({current['wind_mph']} миль/ч)
Порывы до {current['gust_kph']} км/ч ({current['gust_mph']} миль/ч)
Направление ветра: {current['wind_dir']} ({current['wind_degree']} градус)

Облачность: {current['cloud']}%

Качество воздуха:
Стандарт US - EPA: {air_quality['us-epa-index']}

Содержание вредных веществ:

Угарный газ (CO):
{round(air_quality['co'] / 1000, 4)} мг/м3 (Норма: <20 мг/м3

Озон (О3):
{round(air_quality['o3'] / 1000, 4)} мг/м3 (Норма: <0.1 мг/м3)

Диоксид азота (NO2):
{round(air_quality['no2'] / 1000, 4)} мг/м3 (Норма: <0.04 мг/м3)

Диоксид серы (SO2):
{round(air_quality['so2'] / 1000, 4)} мг/м3 (Норма: <0.05 мг/м3)

Мелкодисперсная пыль и аэрозоль размером от 10 мкм до 2,5 мкм.:
{round(air_quality['pm2_5'] / 1000, 4)} мг/м3 (Норма: <{25 / 1000})

Взвешенные крупные твёрдые или жидкие частицы диаметром менее 10 микрометров:
{round(air_quality['pm10'], 4)}
"""


def first_el(st):
    return st.split()[0]


def second_el(st):
    return st.split()[1]


def hour_forecast(data):
    text = ''

    for d in data:
        text += f'{second_el(d["time"])}\n'
        text += f'Температура: {d["temp_c"]} C ({d["temp_f"]} F)\n'
        text += f'Скорость ветра: {d["wind_kph"]} Км/ч ({d["wind_mph"]} Миль/час)\n'
        text += f'Вероятность осадков: {d["chance_of_rain"]}%\n'
        text += f'Облачность: {d["cloud"]}%\n\n'

    return text


def day_forecast(day, forecast, astro):
    return f"""{day['condition']['text']}
    
Средняя влажность: {day['avghumidity']}%
Вероятность осадков: {day['daily_chance_of_rain']}%
    
Средняя температура: {day['avgtemp_c']}C ({day['avgtemp_f']}F)
Максимальная температура: {day['maxtemp_c']}C ({day['maxtemp_f']}F)
Минимальная температура: {day['mintemp_c']}C ({day['mintemp_f']}F)

Восход солнца: {to_normal_time(astro['sunrise'])}
Закат: {to_normal_time(astro['sunset'])}
    
Почасовой прогноз:
    
{hour_forecast(forecast[0]['hour'])}
    
    """


def to_today_forecast(json):
    location = json['location']
    forecast = json['forecast']['forecastday']
    astro = forecast[0]['astro']
    day = forecast[0]['day']

    data = f"""Прогноз погоды на сегодня в {location['name']}
    {day_forecast(day, forecast, astro)}
    """

    return data


def to_tomorrow_forecast(json):
    location = json['location']
    forecast = json['forecast']['forecastday']
    astro = forecast[1]['astro']
    day = forecast[1]['day']

    data = f"""Прогноз погоды на завтра в {location['name']}
        {day_forecast(day, forecast, astro)}
        """

    return data


def to_tomorrow_tomorrow_forecast(json):
    location = json['location']
    forecast = json['forecast']['forecastday']
    astro = forecast[2]['astro']
    day = forecast[2]['day']

    data = f"""Прогноз погоды на послезавтра в {location['name']}
        {day_forecast(day, forecast, astro)}
        """

    return data
