import json
from .config import dataRoot, timePeriodNames

routeDataRoot = dataRoot / "routeData"

# {'st': {}, 'kcm': {'675': {'243': 'Fall 2024'}, '7': {'243': 'Fall 2024'}}}
def buildIndex():
    index = {}
    for agency_dir in routeDataRoot.iterdir():
      if not agency_dir.is_dir():
            continue
      
      agencyIndex = {}
      for route_dir in agency_dir.iterdir():
          if not route_dir.is_dir():
              continue

          route = route_dir.name
          agencyIndex[route] = []

          routeIndex = {}
          for period_dir in route_dir.iterdir():
              data = period_dir / "ridershipData.csv"

              if data.exists():
                  routeIndex[period_dir.name] = timePeriodNames[period_dir.name]
          agencyIndex[route_dir.name] = routeIndex
      index[agency_dir.name] = agencyIndex

    return index

# For testing
#print(buildIndex())