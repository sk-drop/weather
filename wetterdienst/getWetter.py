from wetterdienst import DWDObservationData, Parameter, PeriodType, TimeResolution, DWDObservationSites


# set parameters for less stuffed function calls
params_daily = [Parameter.CLIMATE_SUMMARY, Parameter.PRECIPITATION_MORE,
                Parameter.WATER_EQUIVALENT, Parameter.WEATHER_PHENOMENA]
params_subdaily = [Parameter.WIND, Parameter.CLOUDINESS, Parameter.PRESSURE,
                   Parameter.VISIBILITY, Parameter.MOISTURE]
params_hourly = [Parameter.TEMPERATURE_AIR, Parameter.SOLAR, Parameter.DEW_POINT,
                 Parameter.TEMPERATURE_SOIL, Parameter.WIND_SYNOPTIC]

# get stations who do daily observations
sites_daily = DWDObservationSites(
    parameter=Parameter.CLIMATE_SUMMARY,
    time_resolution=TimeResolution.DAILY,
    period_type=PeriodType.HISTORICAL,
    start_date="2015-01-01",
    end_date="2020-10-10",
)

# same for subdaily (3x per day)
sites_subdaily = DWDObservationSites(
    parameter=Parameter.CLIMATE_SUMMARY,
    time_resolution=TimeResolution.DAILY,
    period_type=PeriodType.HISTORICAL,
    start_date="2015-01-01",
    end_date="2020-10-10",
)

# hourly
sites_hourly = DWDObservationSites(
    parameter=Parameter.CLIMATE_SUMMARY,
    time_resolution=TimeResolution.DAILY,
    period_type=PeriodType.HISTORICAL,
    start_date="2015-01-01",
    end_date="2020-10-10",
)

# wetterdienstobj. to df
sites_daily = sites_daily.all()
sites_subdaily = sites_subdaily.all()
sites_hourly = sites_hourly.all()

# get station ID's
station_ids_d = sites_daily.STATION_ID.unique()
station_ids_s = sites_subdaily.STATION_ID.unique()
station_ids_h = sites_hourly.STATION_ID.unique()

# collect daily observations
observations_daily = DWDObservationData(
    station_ids=station_ids_d,
    parameter=params_daily,
    time_resolution=TimeResolution.DAILY,
    start_date="2015-01-01",
    end_date="2020-10-10",
    tidy_data=True,
    humanize_column_names=True,
)

# collect subdaily
observations_subdaily = DWDObservationData(
    station_ids=station_ids_s,
    parameter=params_subdaily,
    time_resolution=TimeResolution.SUBDAILY,
    start_date="2015-01-01",
    end_date="2020-10-10",
    tidy_data=True,
    humanize_column_names=True,
)

# collect hourly
observations_hourly = DWDObservationData(
    station_ids=station_ids_h,
    parameter=params_hourly,
    time_resolution=TimeResolution.HOURLY,
    start_date="2015-01-01",
    end_date="2020-10-10",
    tidy_data=True,
    humanize_column_names=True,
)

# cache data in files named after their respective ID
for df in observations_hourly.collect_data():
    name = str(df.STATION_ID.iloc[0]).strip(".0")
    df.to_csv('../../'.format(path, "hourly/", name))
    print('{} done'.format(name))

for df in observations_daily.collect_data():
    name = str(df.STATION_ID.iloc[0]).strip(".0")
    df.to_csv('{}{}{}.csv'.format(path, "daily/", name))
    print('{} done'.format(name))

for df in observations_subdaily.collect_data():
    name = str(df.STATION_ID.iloc[0]).strip(".0")
    df.to_csv('{}{}{}.csv'.format(path, "subdaily/", name))
    print('{} done'.format(name))
