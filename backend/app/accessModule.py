
import pandas as pd
from .config import dataRoot

def getRidershipData(agency, routeNum, servicePeriod):
    ridershipDatafilePath = f"{dataRoot}/routeData/{agency}/{routeNum}/{servicePeriod}/ridershipData.csv"
    return pd.read_csv(ridershipDatafilePath)

# For testing
# print(getRidershipData("kcm", "7", "243"))

# Uncomment to print out the results on startup.
# def getAgencyRidership(agency, servicePeriod):
#     for i in range(0, 1000):
#         routeId = str(i)
#         try:
#           df = getRidershipData(agency, routeId, servicePeriod)
#           avgDailyRidershipPerRoute = int(df["dailyBoardings"].sum())
#           print("{0}, {1}".format(routeId, avgDailyRidershipPerRoute))
#         except:
#           continue

# getAgencyRidership("ct", "2510")