# https://github.com/panodata/dwdweather2/
import pandas as pd
from dwdweather import DwdWeather

dwd = DwdWeather(resolution="daily")
stations = dwd.stations()

stationIDs = []
stationNames = []

for station in stations:
    for key, value in station.items():
        if key == "date_end":
            if value > 20200101:
                stationIDs.append(station.get("station_id"))
                stationNames.append(station.get("name"))

# recreating the dates for the past 6 years
pastdates = pd.date_range(start="2015-01-01", end="2020-10-10")

# columns from /blob/master/doc/usage-library.rst
columns = ['stID', 'date', 'prec', 'prec_f', 'prec_h_mm', 'prec_q', 'soil002', 'soil005', 'soil010',
                   'soil020', 'soil050', 'soil100', 'soil_q', 'sun_dur_min', 'sun_sky', 'sun_gl', 'sun_atmo', 'sun_zen',
                   'sun_q', 'sun_dur_ph_min', 'sun_q2', 'air_hum', 'air_temp', 'air_q', 'wind_d', 'wind_s', 'wind_q']

i = 0
for id in stationIDs:
    old = pd.DataFrame(columns=columns)
    for date in pastdates:
        data = dwd.query(id, date)
        new = pd.DataFrame.from_dict(data, orient='index', columns=columns)
        fin = pd.concat([old, new])
        fin.to_csv("./data/{}".format(stationNames[i]))

    i = i + 1




