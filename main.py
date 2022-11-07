#import requests
#7b6086e0fd1b597a93b193c8dc03a8df

import http.client
import json
import streamlit as st
import numpy as np
import pandas as pd
from collections import namedtuple
from array import *



class obj:

    # constructor
    def __init__(self, dict1):
        self.__dict__.update(dict1)

conn = http.client.HTTPSConnection("v3.football.api-sports.io")

headers = {
    'x-rapidapi-host': "v3.football.api-sports.io",
    'x-rapidapi-key': "7b6086e0fd1b597a93b193c8dc03a8df"
    }

#conn.request("GET", "/fixtures/rounds?season=2022&league=2", headers=headers)
conn.request("GET", "/fixtures?league=2&season=2022", headers=headers)

res = conn.getresponse()
data = res.read()

x = json.loads(data.decode("utf-8"))
dataObj = json.loads(json.dumps(x), object_hook=obj)

array2 = []

for match in dataObj.response:

    temp = []

    temp.append(str(match.teams.home.name) + " - " + str(match.teams.away.name))
    temp.append(str(match.goals.home) + " - " + str(match.goals.away))
    array2.append(temp)

# print(dataObj.response[0].fixture.id)
# print(array2)

test = np.array(array2)

df = pd.DataFrame(
    test,
    columns=(["Fixture", "Score"]))

st.dataframe(df)
st.dataframe(df)