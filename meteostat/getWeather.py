import requests
import gzip
import json
import pandas as pd
import io
import os

# getting metafile with info about every registered weatherstation (17.10.2020)
url = "https://bulk.meteostat.net/stations/stations.json.gz"
res = requests.get(url)
open('./data/metaJSON.gz', 'wb').write(res.content)

# reading the file and constructing dataframe
f = gzip.open('data/weatherdata/metaJSON.gz', 'rb')
file = f.read()
f.close()
data = json.loads(file)
df = pd.DataFrame.from_dict(data)

# selecting important data
ddf = df.loc[df['country'] == 'DE']
vipID = ddf['id']
vipName = []

# cleaning names
for c in ddf['name']:
    c = "".join(c.values())
    res = c.replace('([^"]*)', '')
    vipName.append(res)

# caching data from meteostat (17.10.2020)
t = 0
for i in vipID:
    myUrl = "https://bulk.meteostat.net/daily/{}.csv.gz".format(i)
    res = requests.get(myUrl)
    print(res.status_code)
    if res.status_code == 404:
        continue
    open('{}.gz'.format(i), 'wb').write(res.content)
    f = gzip.open('{}.gz'.format(i), 'rb')
    file = f.read()
    f.close()
    os.remove(f.name)
    df = pd.read_csv(io.StringIO(file.decode('utf-8')),
                     names=['date', 'tavg', 'tmin', 'tmax', 'prcp', 'snow',
                            'wdir', 'wspd', 'wspt', 'pres', 'tsun'])
    name = vipName[t].replace(" ", "").replace("/", "+")
    df.to_csv(r'~/PycharmProjects/weather/data/{}.csv'.format(name))
    t = t + 1

