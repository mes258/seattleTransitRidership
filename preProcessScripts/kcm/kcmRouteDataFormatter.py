import os
import csv

# Input the time period and route number (optional)
# Read from the raw data file
# Read from the stops file
# Write ouput to new data.csv in the data folder

# Replace with the actual file path
rawDataFilePath = "../../data/rawData/kcm/243_Fall_2024_Summarized_Stop_Data.csv"
#rawDataFilePath = "../../data/rawData/kcm/241_Spring_2024_Stop_Summary_Data.csv"
# Set accordingly
timePeriod = "243"
# Set to None for all routes to be populated
route = "550" 


# Stop data
def readKcmStopFile():
    stopData = []
    stopDataFilePath = "../../data/stopData/kcm/allStops.txt"

    try: 
      with open(stopDataFilePath, mode='r', newline='') as infile:
        reader = csv.DictReader(infile)
        for row in reader:
          stopData.append(row)
    except:
      return stopData
    return stopData

def getKcmStopNameForStopId(stopData, stopId):
    for stopRow in stopData:
        if stopRow["stop_id"] == stopId:
            return stopRow["stop_name"]
    return "NOT FOUND"


# Open the input CSV file
with open(rawDataFilePath, mode='r', newline='') as infile:
    reader = csv.DictReader(infile)
    
    stopData = readKcmStopFile()

    for row in reader:
        # input schema: SERVICE_CHANGE_NUM,CHANGE_NUM,STOP_ID,STOP_SEQUENCE_NUM,DAY_PART_CD,SERVICE_RTE_NUM,
        # EXPRESS_LOCAL_CD,INBD_OUTBD_CD,HOST_STREET_NM,CROSS_STREET_NM,STOP_PLACEMENT_CD,TRIP_COMPASS_DIR_CD,
        # JURISDICTION_CD,OBSERVED_TRIPS_IDS,TOTAL_OBSERVATIONS,AVG_TRIP_BOARDINGS,AVG_TOTAL_BOARDINGS,
        # AVG_TRIP_ALIGHTINGS,AVG_TOTAL_ALIGHTINGS,AVG_TRIP_DEPARTING_LOAD

        # Extract SERVICE_CHANGE_NUM and SERVICE_RTE_NUM values
        service_change_num = row['SERVICE_CHANGE_NUM']
        service_rte_num = row['SERVICE_RTE_NUM']
        
        if service_change_num == timePeriod and (service_rte_num == route or route is None):
          stopName = getKcmStopNameForStopId(stopData, row['STOP_ID'])
          if stopName == "NOT FOUND":
            print(f"Stop Name not found: route: {service_rte_num}, stop: {row['STOP_ID']}")
            stopName = f"{row['HOST_STREET_NM']} & {row['CROSS_STREET_NM']}"

          if row['STOP_SEQUENCE_NUM'] == "NULL":
            print(f"stop {row['STOP_ID']} has no stop sequence, will skip it")
            continue

          outputRow = {"serviceChangeNum": row['SERVICE_CHANGE_NUM'],
                       "routeNum": row['SERVICE_RTE_NUM'],
                       "direction": row['INBD_OUTBD_CD'],
                       "stopId": row['STOP_ID'],
                       "stopName": stopName,
                       "stopOrderNum": row['STOP_SEQUENCE_NUM'],
                       "timeOfDay": row['DAY_PART_CD'],
                       "tripBoardings": row['AVG_TRIP_BOARDINGS'],
                       "tripAlightings": row['AVG_TRIP_ALIGHTINGS'],
                       "departingLoad": row['AVG_TRIP_DEPARTING_LOAD'],
                       "dailyBoardings": row['AVG_TOTAL_BOARDINGS'],
                       "dailyAlightings": row['AVG_TOTAL_ALIGHTINGS']
                       }

          # Create the directory path based on SERVICE_CHANGE_NUM and SERVICE_RTE_NUM
          # eg: data/routeData/kcm/7/243
          directory = f"../../data/routeData/kcm/{service_rte_num}/{service_change_num}"
          if service_rte_num[0] == "5":
            print("st route)")
            directory = f"../../data/routeData/st/{service_rte_num}/{service_change_num}"
          
          os.makedirs(directory, exist_ok=True)
          
          # Define the output file path
          output_file = os.path.join(directory, 'ridershipData.csv')
          
          # Check if the file already exists to determine whether to write the header
          file_exists = os.path.isfile(output_file)
          
          # Write the row to the appropriate stopLevelData.csv file
          with open(output_file, mode='a', newline='') as outfile:
              fieldnames = ['serviceChangeNum', 'routeNum', 'direction', 'stopId', 'stopName', 'stopOrderNum', 'timeOfDay', 'tripBoardings', 'tripAlightings', 'departingLoad', 'dailyBoardings', 'dailyAlightings']

              writer = csv.DictWriter(outfile, fieldnames=fieldnames)
              if not file_exists:
                  writer.writeheader()  # Write the header if the file does not exist
              writer.writerow(outputRow)

