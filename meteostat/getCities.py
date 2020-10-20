# https://www.destatis.de/DE/Themen/Laender-Regionen/Regionales/Gemeindeverzeichnis/Administrativ/08-gemeinden-einwohner-groessen.html
import pandas as pd
import re

pd.set_option('display.max_columns', None)

xls = pd.ExcelFile("./data/AuszugGV3QAktuell.xlsx")
df = pd.read_excel(xls, "Onlineprodukt_Gemeinden", skiprows=1, dtype={'Postleitzahl3':str})

# drop columns we're not interested in
df = df.dropna()
df = df.drop(df.columns[0:7], axis=1)
df = df.drop(df.columns[[9, 11]], axis=1)

# rename
df.columns = ['name', 'km^2', 'bev', 'm', 'w', 'dichte',
              'plz', 'longitude', 'latitude', 'reiseGebiete',
              'verstädterung']

pattern = ",[\s](Stadt)|,[\s](\w*stadt)|(\((.+?)\))|(\/.+)$"
df['name'] = [re.sub(pattern, '', name) for name in df['name']]
print(df['name'])

df.to_csv('./data/gerZones.csv')