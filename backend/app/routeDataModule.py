
from .config import rapidRideRouteMapping, stbKcmUrl
import json 

def getAvgWeekdayRidership(df):
  return int(df["dailyBoardings"].sum())

def getMetroScheduleUrl(route):
  baseUrl = "https://kingcounty.gov/en/dept/metro/routes-and-service/schedules-and-maps"
  urlRoute = f"{int(route):03d}"
  if urlRoute in rapidRideRouteMapping:
    urlRoute = rapidRideRouteMapping[urlRoute]
  scheduleUrl = f"{baseUrl}/{urlRoute}"
  return scheduleUrl

def getStScheduleUrl(route):
  baseUrl = "https://www.soundtransit.org/ride-with-us/routes-schedules"
  scheduleUrl = f"{baseUrl}/{route}"
  return scheduleUrl

def getScheduleUrl(agency, route):
  if agency == "kcm":
    return getMetroScheduleUrl(route)
  if agency == "st":
    return getStScheduleUrl(route)
  return ""

def getStbUrl(agency, route):
  if agency == "kcm":
    if route in stbKcmUrl:
      return stbKcmUrl[route]
  
  return ""

def getRouteName(agency, route):
  routeName = f"Route {route}"
  if agency == "kcm":
    if route in rapidRideRouteMapping:
      parts = rapidRideRouteMapping[route].split("-")
      routeName = f"{parts[0].upper()} {parts[1].title()}"
  
  return routeName


# The json object stored for each route that has:
# Metro schedule URL, 
# STB post URL (if possible)
# Average weekday ridership (sum of dailyBoardings)
# TODO: Add key route destinations
def buildRouteData(df, agency, route):
  rtnJson = {}
  rtnJson["avgWeekdayRidership"] = getAvgWeekdayRidership(df)
  rtnJson["scheduleUrl"] = getScheduleUrl(agency, route)
  rtnJson["stbUrl"] = getStbUrl(agency, route)
  rtnJson["routeName"] = getRouteName(agency, route)

  return json.dumps(rtnJson)
