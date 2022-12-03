import http.client
import json
import requests
import streamlit.components.v1 as components
import streamlit as st
import pandas as pd
from datetime import datetime
from streamlit_lottie import st_lottie
from PIL import ImageColor
#############################################################################
# Global Variables
#############################################################################
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
# Initial page setup
#############################################################################
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

#############################################################################
# Obj to fill JSON data from requests
#############################################################################
class obj:

    # constructor
    def __init__(self, dict1):
        self.__dict__.update(dict1)

###############################################################################
#Request to get Fixture Data
#############################################################################
conn = http.client.HTTPSConnection("v3.football.api-sports.io")

headers = {
    'x-rapidapi-host': "v3.football.api-sports.io",
    'x-rapidapi-key': "7b6086e0fd1b597a93b193c8dc03a8df"
    }

conn.request("GET", "/fixtures?league=2&season=2022", headers=headers)

res = conn.getresponse()
data = res.read()

temp = json.loads(data.decode("utf-8"))
fixtureData = json.loads(json.dumps(temp), object_hook=obj)

###########################################################################
# Request for List of teams
#############################################################################

conn.request("GET", "/teams?league=2&season=2022", headers=headers)

res = conn.getresponse()
data = res.read()

y = json.loads(data.decode("utf-8"))
teamsList = json.loads(json.dumps(y), object_hook=obj)

teamOptions = []

for team in teamsList.response:
    teamOptions.append(team.team.name)

###############################################################################
#Fill Map Code
#############################################################################
def fillMap():

    for venue in venueList:
        ################################################################################
        # Request to get adress of venues
        ################################################################################

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
        mapData["lat"].append(venueData["results"][0]["lat"])
        mapData["lon"].append(venueData["results"][0]["lon"])

    tempDf = pd.DataFrame.from_dict(mapData, orient= 'columns')
    return tempDf

#############################################################################
#Fill Data Frame Code
#############################################################################
def fillDataFrame():

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
#Fill Line Chart Code
#############################################################################
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
                lineChartData[homeTeam].append(homeTeamGoals + (lineChartData[homeTeam][len(lineChartData[homeTeam]) - 1] * len(lineChartData[homeTeam])))
                lineChartData[homeTeam][len(lineChartData[homeTeam]) - 1] /= len(lineChartData[homeTeam])


            if awayTeam not in lineChartData:
                lineChartData[awayTeam] = [awayTeamGoals]
            else:
                lineChartData[awayTeam].append(awayTeamGoals + (lineChartData[awayTeam][len(lineChartData[awayTeam]) - 1] * len(lineChartData[awayTeam])))
                lineChartData[awayTeam][len(lineChartData[awayTeam]) - 1] /= len(lineChartData[awayTeam])

    tempDf = pd.DataFrame.from_dict(lineChartData, orient= 'index')
    tempDf = tempDf.transpose()
    tempDf = tempDf.rename(index=lambda x: int(x+1))

    return tempDf

###############################################################################
#Fill Bar Chart Code
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

    tempDf = pd.DataFrame.from_dict(barChartData, orient='index')
    tempDf = tempDf.transpose()
    tempDf = tempDf.rename(index=lambda x: int(x + 1))

    return tempDf

#############################################################################
#Lottie Image Code
#############################################################################

def load_lottieurl(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

lottie_coding = load_lottieurl("https://assets2.lottiefiles.com/packages/lf20_ky03n5aXvs.json")

#############################################################################
#Loading Data
#############################################################################

df = fillDataFrame()
lc = fillLineChart()
bc = fillBarChart()

#############################################################################
#Data Frame code
#############################################################################

filteredTeams = st.multiselect('Select Team(s):', options=teamOptions, default="Paris Saint Germain")

if st.button('Help?'):
    st.info('Hit the dropdown and select any teams you would like to know information about in the Champions League', icon="ℹ️")


if len(filteredTeams) == 0:
    st.warning('Warning no team selected!!', icon="⚠️")

with st.container():
    st.write("---")
    st.header("Data Frame")
    bar_column, line_column, test_column = st.columns((1,2,2))
    with bar_column:
        filteredMatches = st.radio("Filter Data Table by outcome: ", ("All", "Home Team Wins", "Away Team Wins", "Draw"))
    with line_column:
        datetime_str = '22/01/01'
        datetime_object = datetime.strptime(datetime_str, '%y/%m/%d')
        filteredFromDate = st.date_input("From Date", value=datetime_object)
        color = st.color_picker('Pick a color for table:', '#FFFFFF')
    with test_column:
        filteredToDate = st.date_input("To Date")
        textColor = st.color_picker('Pick a color for table text:', '#000000')

df_selection = df.query("`Home Team` == @filteredTeams | `Away Team` == @filteredTeams")

match filteredMatches:
    case "Home Team Wins":
        df_selection = df_selection.query("`Home Team Goals` > `Away Team Goals`")
    case "Away Team Wins":
        df_selection = df_selection.query("`Home Team Goals` < `Away Team Goals`")
    case "Draw":
        df_selection = df_selection.query("`Home Team Goals` == `Away Team Goals`")

df_selection["Date"] = pd.to_datetime(df_selection['Date'])
df_selection["Date"] = df_selection['Date'].dt.date
df_selection = df_selection.query("@filteredFromDate <= `Date` <= @filteredToDate")
lc_selection = lc.loc[:,filteredTeams]
bc_selection = bc.loc[:,filteredTeams]


with st.container():
    dataFrame_column, lottie_column = st.columns((3,1))
    with dataFrame_column:
        if len(filteredTeams) == 0:
            st.error('Error!! No team provided!!', icon="🚨")
        else:
            temp = ImageColor.getcolor(color,"RGB")
            tempText = ImageColor.getcolor(textColor, "RGB")
            colorStr = "rgb(" + str(temp[0]) + "," + str(temp[1]) + "," + str(temp[2]) + ")"
            textColorStr = "rgb(" + str(tempText[0]) + "," + str(tempText[1]) + "," + str(tempText[2]) + ")"
            st.dataframe(df_selection.style.set_properties(**{'background-color': colorStr, 'color': textColorStr}))

    with lottie_column:
        st_lottie(lottie_coding, width= 350, key="coding")

#################################################################################
# Bar Chart and Line Chart Code
#################################################################################
with st.container():
    st.write("---")
    bar_column, line_column = st.columns((1,1))
    with bar_column:
        st.header("Bar Chart - Goals per game")
        if len(filteredTeams) == 0:
            st.error('Error!! No team provided!!', icon="🚨")
        else:
            st.bar_chart(bc_selection)

    with line_column:
        st.header("Line Chart - Average Goals per game")
        if len(filteredTeams) == 0:
            st.error('Error!! No team provided!!', icon="🚨")
        else:
            st.line_chart(lc_selection)

    st.write("---")

#################################################################################
# Champions League Standing Code
#################################################################################

st.header("Champions League Standings")
displayStandings = st.checkbox("Display Champions League Standings")
if displayStandings:
    HtmlFile = open("index.html", 'r', encoding='utf-8')
    source_code = HtmlFile.read()
    print(source_code)
    components.html(source_code, height= 1000)
st.write("---")

#################################################################################
# Map - Stadiums Played Code
#################################################################################

st.header("Map - Stadiums Played")
displayStandings = st.checkbox("Display Champions League Venue Map")
if displayStandings:
    mp = fillMap()
    st.map(mp)
st.write("---")

option = st.selectbox('How did you find the user interface?',('','Perfect', 'Good', 'Could be better', 'Bad'))

#################################################################################
# Feedback Code
#################################################################################

if option is not '':
    st.write('Thank you for your feedback.')