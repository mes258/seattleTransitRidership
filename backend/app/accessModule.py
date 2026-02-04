
import pandas as pd
from .config import dataRoot

def getRidershipData(agency, routeNum, servicePeriod):
    ridershipDatafilePath = f"{dataRoot}/routeData/{agency}/{routeNum}/{servicePeriod}/ridershipData.csv"
    return pd.read_csv(ridershipDatafilePath)

# For testing
#print(getRidershipData("kcm", "7", "243"))