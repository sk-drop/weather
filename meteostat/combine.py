import os
import pandas as pd
import re

# load german commune data for county code and variables like population, density, etc.
ger = pd.read_csv("./data/gerZones.csv", dtype={"plz": str})

# threshold date
d = pd.to_datetime("2015-01-01").date()


# df for all weather data
cols = ['date', 'tavg', 'tmin', 'tmax', 'prcp', 'snow',
        'wdir', 'wspd', 'wspt', 'pres', 'tsun']
all = pd.DataFrame(columns=cols)


# testing for string equality
def stringEQ(str1, str2):
    if len(str1) > len(str2):
        big = str1
        sml = str2
    else:
        big = str2
        sml = str1
    if sml in big:
        return True
    else:
        return False


# replacement function
def replacer(tx, dic):
    for i, j in dic:
        tx = tx.replace(i, j)
    return tx


# dictionary with replacement values
od = ([('ue', 'ü'), ('oe', 'ö'), ('ae', 'ä'), ('+', '-'), ('.csv', '')])


# iterating through files
for i in os.listdir("./data/weatherdata"):

    # replace
    j = replacer(i, od)
    # check string eq
    print(j)
    matches = [stringEQ(name, j) for name in ger['name']]
    matches = ger.name[matches]
    if not matches.any():
        continue
    elif len(matches) == 1:
        print(matches)
        tdf = pd.read_csv("./data/weatherdata/{}".format(i))
        print("match found")
    else:
        continue

    # sort out dates earlier than threshold
    tdf.date = [pd.to_datetime(date, errors='coerce').date() for date in tdf.date]
    vipD = [date >= d for date in tdf.date]
    tdf.date = tdf.date[vipD]

    # combine commune info with weather info & clean cols
    ndf = ger.iloc[matches.index]
    tdf = pd.concat([tdf, ndf], axis=1)
    tdf = tdf.loc[:, ~tdf.columns.duplicated()]
    # pandas somehow adds index-like columns named: Unnamed
    tdf = tdf[tdf.columns.drop(list(tdf.filter(regex='Unn*')))]
    all = pd.concat([all, tdf])

    # save to final file
    filename = "".join(ndf['plz'])
    if "{}.csv".format(filename) in os.listdir("./data/weatherdata/final"):
        tdf.to_csv("./data/weatherdata/final/{}_1.csv".format(filename))
    else:
        tdf.to_csv("./data/weatherdata/final/{}.csv".format(filename))
    print("{} done".format(j))

all.to_csv("./data/allweather.csv")
