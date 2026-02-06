from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pathlib import Path
from .dataIndex import buildIndex
from .accessModule import getRidershipData
from .graphModule import plotTripRidership, plotDailyRidership
from .routeDataModule import buildRouteData
from .config import dataRoot
import json

dataIndex = buildIndex()
baseDir = Path(__file__).resolve().parent
frontendDir = baseDir.parent.parent / "frontend"

app = FastAPI()

# Mount static files (index, about, favicon)
app.mount(
    "/frontend",
    StaticFiles(directory=frontendDir, html=True),
    name="frontend",
)

@app.get("/")
def index():
    return FileResponse(frontendDir / "index.html")

@app.get("/about")
def about():
    return FileResponse(frontendDir / "about.html")

@app.get("/favicon.ico")
def index():
    return FileResponse(frontendDir / "favicon.ico")

@app.get("/api/agencies")
def getAgencies():
    return sorted(dataIndex.keys())

@app.get("/api/agencies/{agency}/routes")
def getRoutes(agency: str):
    if agency not in dataIndex:
        raise HTTPException(404, "Agency not found")
    routeList = sorted(dataIndex[agency].keys())
    sortedRouteList = sorted(
      routeList,
      key=lambda x: (not (670 <= int(x) <= 699), int(x))
    )
    return sortedRouteList

@app.get("/api/agencies/{agency}/routes/{route}/serviceChanges")
def getServiceChanges(agency: str, route: str):
    if agency not in dataIndex or route not in dataIndex[agency]:
        raise HTTPException(404, "Route not found")
    serviceChangeList = list(reversed(sorted(dataIndex[agency][route].keys())))
    return serviceChangeList

@app.get("/api/ridershipCharts")
def getAllCharts(agency: str, route: str, serviceChange: str):
    if agency not in dataIndex or route not in dataIndex[agency] or serviceChange not in dataIndex[agency][route]:
      raise HTTPException(404, "Route or service period not found")
    
    serviceChangePath = dataRoot / "routeData" / agency / route / serviceChange
    
    rtnJson = {}
    tripPlotJson = None
    dailyPlotJson = None

    # Read the data to be used in plot generation
    ridershipData = getRidershipData(agency, route, serviceChange)

    # Trip Ridership: 
    # Check if the plot json is already stored for these parameters
    tripPlotJsonPath = serviceChangePath / "tripRidershipPlot.json"
    if tripPlotJsonPath.exists():
      # Use the existing json data
      f = open(tripPlotJsonPath, "r")
      tripPlotJson = json.load(f)
      f.close()
    else:
      # Generate the plot json (and write to a file)
      tripPlotJson = plotTripRidership(ridershipData, route, serviceChange)
      with open(tripPlotJsonPath, "w") as outfile:
        json.dump(tripPlotJson, outfile)

    rtnJson["tripPlotJson"] = json.loads(tripPlotJson)

    # Daily Ridership: 
    # Check if the plot json is already stored for these parameters
    dailyPlotJsonPath = serviceChangePath / "dailyRidershipPlot.json"
    if dailyPlotJsonPath.exists():
      # Use the existing json data
      f = open(dailyPlotJsonPath, "r")
      dailyPlotJson = json.load(f)
      f.close()
    else:
      # Generate the plot json (and write to a file)
      dailyPlotJson = plotDailyRidership(ridershipData, route, serviceChange)
      with open(dailyPlotJsonPath, "w") as outfile:
        json.dump(dailyPlotJson, outfile)

    rtnJson["dailyPlotJson"] = json.loads(dailyPlotJson)

    # Route Metadata
    # Check if the route data json is already stored for these parameters
    routeDataJsonPath = serviceChangePath / "routeData.json"
    overwriteRouteData = False
    if routeDataJsonPath.exists() and not overwriteRouteData:
      # Use the existing json data
      f = open(routeDataJsonPath, "r")
      routeDataJson = json.load(f)
      f.close()
    else:
      # Generate the plot json (and write to a file)
      routeDataJson = buildRouteData(ridershipData, agency, route)
      with open(routeDataJsonPath, "w") as outfile:
        json.dump(routeDataJson, outfile)

    rtnJson["routeDataJson"] = json.loads(routeDataJson)

    return rtnJson