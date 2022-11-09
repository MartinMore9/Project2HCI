#import requests
#7b6086e0fd1b597a93b193c8dc03a8df
import http.client
import json
import requests
import streamlit.components.v1 as components
import time

import streamlit as st
import numpy as np
import pandas as pd
from datetime import datetime
from dateutil.relativedelta import relativedelta
from datetime import timezone
from collections import namedtuple
from array import *
###############################################################
venueList = set()
mapData = {
    "lat": [],
    "lon": []
}
lineChartData = {}
barChartData = {}
dataFrameData = {
    "Round": [],
    "Home Team": [],
    "Away Team": [],
    "Home Team Goals": [],
    "Away Team Goals": [],
    "Final Score": [],
    "Referee": [],
    "Stadium": [],
    "Date": [],
    "Time UTC": []
}
###############################################################
st.set_page_config(
    page_title= "2022 Champions League",
    page_icon = ":soccer:",
    layout = "wide",
    menu_items ={
        'Get Help' : 'https://docs.streamlit.io',
        'About' : "Welcome to Carolina Valenzuela's, Martin Moreano's, Amanda Chacin-Livinalli's, Richard Uriarte Streamlit HCI Project."
                  "For this project we used the Football API: https://www.api-football.com/ "
    }
)
st.title(":soccer: 2022 Champions League")
st.text("For this project we used the Football API: https://www.api-football.com/")
###############################################################
class obj:

    # constructor
    def __init__(self, dict1):
        self.__dict__.update(dict1)

################################################################

# def updateDataFrame():
#     dataFrameOBJ = st.empty()
#     fillDataFrame()
#     dataFrameOBJ= st.dataframe(dataFrameData)

################################################################

# def fillMap():
#
#     for venue in venueList:
#
#         # tempstr = "/venues?name=" + str(venue)
#         # tempstr = tempstr.replace(" ", "%20")
#         # tempstr = tempstr.encode('ascii', 'ignore').decode('ascii')
#
#         conn.request("GET", "/venues?id=" + str(venue), headers=headers)
#
#         res = conn.getresponse()
#         data = res.read()
#
#         y = json.loads(data.decode("utf-8"))
#         venuesListObj = json.loads(json.dumps(y), object_hook=obj)
#
#         ################################################################################
#
#         name = str(venuesListObj.response[0].name).replace(" ","%20")
#         address = str(venuesListObj.response[0].address).replace(" ","%20")
#         city = str(venuesListObj.response[0].city).replace(" ", "%20")
#         country = str(venuesListObj.response[0].country).replace(" ", "%20")
#
#         url = "https://api.geoapify.com/v1/geocode/search?name=" + name +"&street=" + address +"&city="+ city +"&country="+ country +"&limit=1&format=json&apiKey=4136e494e7a14ee28368c1191cdac050"
#
#         response = requests.get(url)
#         venueData = response.json()
#         # print(response.json())
#         # temp = json.loads(response.json())
#         # venueData = json.loads(json.dumps(temp), object_hook=obj)
#         #print(venueData)
#         mapData["lat"].append(venueData["results"][0]["lat"])
#         mapData["lon"].append(venueData["results"][0]["lon"])
#
#     tempDf = pd.DataFrame.from_dict(mapData, orient= 'columns')
#     return tempDf

###############################################################################

conn = http.client.HTTPSConnection("v3.football.api-sports.io")

headers = {
    'x-rapidapi-host': "v3.football.api-sports.io",
    'x-rapidapi-key': "7b6086e0fd1b597a93b193c8dc03a8df"
    }

#conn.request("GET", "/fixtures/rounds?season=2022&league=2", headers=headers)
conn.request("GET", "/fixtures?league=2&season=2022", headers=headers)

res = conn.getresponse()
data = res.read()

temp = json.loads(data.decode("utf-8"))
fixtureData = json.loads(json.dumps(temp), object_hook=obj)

###############################################################################


###########################################################################

conn.request("GET", "/teams?league=2&season=2022", headers=headers)

res = conn.getresponse()
data = res.read()

y = json.loads(data.decode("utf-8"))
teamsList = json.loads(json.dumps(y), object_hook=obj)

teamOptions = []

for team in teamsList.response:
    teamOptions.append(team.team.name)

###############################################################################
def fillMap():

    for venue in venueList:

        # tempstr = "/venues?name=" + str(venue)
        # tempstr = tempstr.replace(" ", "%20")
        # tempstr = tempstr.encode('ascii', 'ignore').decode('ascii')

        conn.request("GET", "/venues?id=" + str(venue), headers=headers)

        res = conn.getresponse()
        data = res.read()

        y = json.loads(data.decode("utf-8"))
        venuesListObj = json.loads(json.dumps(y), object_hook=obj)

        ################################################################################

        name = str(venuesListObj.response[0].name).replace(" ","%20")
        address = str(venuesListObj.response[0].address).replace(" ","%20")
        city = str(venuesListObj.response[0].city).replace(" ", "%20")
        country = str(venuesListObj.response[0].country).replace(" ", "%20")

        url = "https://api.geoapify.com/v1/geocode/search?name=" + name +"&street=" + address +"&city="+ city +"&country="+ country +"&limit=1&format=json&apiKey=4136e494e7a14ee28368c1191cdac050"

        response = requests.get(url)
        venueData = response.json()
        # print(response.json())
        # temp = json.loads(response.json())
        # venueData = json.loads(json.dumps(temp), object_hook=obj)
        #print(venueData)
        mapData["lat"].append(venueData["results"][0]["lat"])
        mapData["lon"].append(venueData["results"][0]["lon"])

    tempDf = pd.DataFrame.from_dict(mapData, orient= 'columns')
    return tempDf

#############################################################################

def fillDataFrame():
    #filteredData = []

    for match in fixtureData.response:

        if match.fixture.venue.id is not None:

            venueList.add(int(match.fixture.venue.id))

        if str(match.fixture.status.short) == "FT":

            dataFrameData["Round"].append(str(match.league.round))
            dataFrameData["Home Team"].append(str(match.teams.home.name))
            dataFrameData["Away Team"].append(str(match.teams.away.name))
            dataFrameData["Home Team Goals"].append(str(match.goals.home))
            dataFrameData["Away Team Goals"].append(str(match.goals.away))
            dataFrameData["Final Score"].append(str(match.goals.home) + " - " + str(match.goals.away))
            dataFrameData["Referee"].append(str(match.fixture.referee))
            dataFrameData["Stadium"].append(str(match.fixture.venue.name))
            dataFrameData["Date"].append(str(match.fixture.date).split("T")[0])
            dataFrameData["Time UTC"].append(str(match.fixture.date).split("T")[1].split("+")[0])

    tempDf = pd.DataFrame(dataFrameData)

    return tempDf

###############################################################################
def fillLineChart():
    #filteredData = []

    for match in fixtureData.response:

        if str(match.fixture.status.short) == "FT":

            homeTeam = str(match.teams.home.name)
            awayTeam = str(match.teams.away.name)
            homeTeamGoals = 0 if match.goals.home is None else int(match.goals.home)
            awayTeamGoals = 0 if match.goals.home is None else int(match.goals.away)

            if homeTeam not in lineChartData:
                lineChartData[homeTeam] = [homeTeamGoals]
            else:
                #lineChartData[homeTeam].append(homeTeamGoals + lineChartData[homeTeam][len(lineChartData[homeTeam]) - 1])
                lineChartData[homeTeam].append(homeTeamGoals + (lineChartData[homeTeam][len(lineChartData[homeTeam]) - 1] * len(lineChartData[homeTeam])))
                lineChartData[homeTeam][len(lineChartData[homeTeam]) - 1] /= len(lineChartData[homeTeam])


            if awayTeam not in lineChartData:
                lineChartData[awayTeam] = [awayTeamGoals]
            else:
                #lineChartData[awayTeam].append(awayTeamGoals + lineChartData[awayTeam][len(lineChartData[awayTeam]) - 1])
                lineChartData[awayTeam].append(awayTeamGoals + (lineChartData[awayTeam][len(lineChartData[awayTeam]) - 1] * len(lineChartData[awayTeam])))
                lineChartData[awayTeam][len(lineChartData[awayTeam]) - 1] /= len(lineChartData[awayTeam])

    #print(lineChartData)
    #tempDf = pd.DataFrame(lineChartData)
    #tempDf = pd.DataFrame([lineChartData])
    tempDf = pd.DataFrame.from_dict(lineChartData, orient= 'index')
    tempDf = tempDf.transpose()
    tempDf = tempDf.rename(index=lambda x: int(x+1))
    #print(tempDf)
    #tempDf = pd.DataFrame.from_dict(lineChartData, orient='index')

    return tempDf

###############################################################################

def fillBarChart():

    for match in fixtureData.response:

        if str(match.fixture.status.short) == "FT":

            homeTeam = str(match.teams.home.name)
            awayTeam = str(match.teams.away.name)
            homeTeamGoals = 0 if match.goals.home is None else int(match.goals.home)
            awayTeamGoals = 0 if match.goals.home is None else int(match.goals.away)

            if homeTeam not in barChartData:
                barChartData[homeTeam] = [homeTeamGoals]
            else:
                barChartData[homeTeam].append(homeTeamGoals)

            if awayTeam not in barChartData:
                barChartData[awayTeam] = [awayTeamGoals]
            else:
                barChartData[awayTeam].append(awayTeamGoals)

    # print(lineChartData)
    # tempDf = pd.DataFrame(lineChartData)
    # tempDf = pd.DataFrame([lineChartData])
    tempDf = pd.DataFrame.from_dict(barChartData, orient='index')
    tempDf = tempDf.transpose()
    tempDf = tempDf.rename(index=lambda x: int(x + 1))
    #print(tempDf)
    # tempDf = pd.DataFrame.from_dict(lineChartData, orient='index')

    return tempDf

#############################################################################

df = fillDataFrame()
lc = fillLineChart()
bc = fillBarChart()

#############################################################################


st.sidebar.title("Filters")
filteredTeams = st.sidebar.multiselect('Select Team(s):', options=teamOptions, default="Paris Saint Germain")
filteredMatches = st.sidebar.radio("Filter Data Table by outcome: ", ("All", "Home Team Wins", "Away Team Wins", "Draw"))
#displayStandings = st.sidebar.checkbox("Display Champions League Standings")

datetime_str = '22/01/01'
datetime_object = datetime.strptime(datetime_str, '%y/%m/%d')
filteredFromDate = st.sidebar.date_input("From Date", value= datetime_object)
filteredToDate = st.sidebar.date_input("To Date")

#################################################################################

# st.sidebar.title("Filters:")
# filteredTeams = st.sidebar.multiselect('Select Team(s):', options=teamOptions, default="Paris Saint Germain")

df_selection = df.query("`Home Team` == @filteredTeams | `Away Team` == @filteredTeams")

match filteredMatches:
    case "Home Team Wins":
        df_selection = df_selection.query("`Home Team Goals` > `Away Team Goals`")
    case "Away Team Wins":
        df_selection = df_selection.query("`Home Team Goals` < `Away Team Goals`")
    case "Draw":
        df_selection = df_selection.query("`Home Team Goals` == `Away Team Goals`")

#df_selection = df_selection.query("@filteredFromDate <= `Date`")
#print(df_selection.where())
df_selection["Date"] = pd.to_datetime(df_selection['Date'])
df_selection["Date"] = df_selection['Date'].dt.date
df_selection = df_selection.query("@filteredFromDate <= `Date` <= @filteredToDate")
#df_selection = df_selection["Date"].between(filteredFromDate, filteredToDate)
print(df_selection)

#df_selection = df_selection.query("")
#lc_selection = lc.query(index = "@filteredTeams")
#lc_selection = lc.loc[0].loc[filteredTeams]
lc_selection = lc.loc[:,filteredTeams]
bc_selection = bc.loc[:,filteredTeams]
#lc_selection = lc.loc[filteredTeams]
#lc_selection = lc_selection.
#print(lc_selection)
#print(venueList)
st.header("Data Frame")
st.dataframe(df_selection)
#st.dataframe(bc_selection)
# st.header("Bar Chart - Goals per game")
# st.bar_chart(bc_selection)
# #st.dataframe(lc_selection)
# st.header("Line Chart - Average Goals per game")
# st.line_chart(lc_selection)


with st.container():
    st.write("---")
    bar_column, line_column = st.columns((1,1))
    with bar_column:
        st.header("Bar Chart - Goals per game")
        st.bar_chart(bc_selection)
    with line_column:
        st.header("Line Chart - Average Goals per game")
        st.line_chart(lc_selection)
    st.write("---")

st.header("Champions League Standings")
displayStandings = st.checkbox("Display Champions League Standings")
if displayStandings:
    HtmlFile = open("index.html", 'r', encoding='utf-8')
    source_code = HtmlFile.read()
    print(source_code)
    components.html(source_code, height= 1000)
st.write("---")

st.header("Map - Stadiums Played")
displayStandings = st.checkbox("Display Champions League Venue Map")
if displayStandings:
    mp = fillMap()
    st.map(mp)
st.write("---")

# mp = fillMap()
# st.map(mp)


#print(mapData)
