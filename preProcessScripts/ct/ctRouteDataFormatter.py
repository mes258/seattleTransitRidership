import csv
from datetime import datetime
from collections import defaultdict
import os

def get_day_type(date):
    day = date.strftime("%A")
    if day == "Saturday":
        return "Saturday"
    elif day == "Sunday":
        return "Sunday"
    else:
        return "Weekday"

def get_time_period(time_str):
    time = datetime.strptime(time_str, "%H:%M:%S").time()
    if time < datetime.strptime("05:00:00", "%H:%M:%S").time():
        return "XNT"
    elif time < datetime.strptime("09:00:00", "%H:%M:%S").time():
        return "AM"
    elif time < datetime.strptime("15:00:00", "%H:%M:%S").time():
        return "MID"
    elif time < datetime.strptime("19:00:00", "%H:%M:%S").time():
        return "PM"
    elif time < datetime.strptime("22:00:00", "%H:%M:%S").time():
        return "XEV"
    else:
        return "XNT"
    
def get_direction_code(direction:str, routeId:str):
    if direction.lower() == "north" or direction.lower() == "east":
      return "I"
    else:
        return "O"

# Read CSV file
def get_input_data(filePath:str):
  # OPERATION_DATE,ROUTE_ID,DIRECTION,TRIP_ID,VEHICLE_ID,SCHED_DEPTIME,ACT_ARRTIME,ACT_DEPTIME,STOP_ORDER_NBR,STOP_ID,STOP,BOARDINGS,ALIGHTINGS

  data = []
  with open(filePath, "r") as file:
      reader = csv.DictReader(file)
      for row in reader:
          if row["ACT_DEPTIME"] and row["OPERATION_DATE"]:
              try:
                  date_obj = datetime.strptime(row["OPERATION_DATE"], "%Y-%m-%d").date()
                  row["DATE"] = date_obj
                  row["DAY_TYPE"] = get_day_type(date_obj)
                  row["ALIGHTINGS"] = float(row["ALIGHTINGS"])
                  row["BOARDINGS"] = float(row["BOARDINGS"])
                  row["TIME_PERIOD"] = get_time_period(row["ACT_DEPTIME"])
                  row["DIRECTION"] = get_direction_code(row["DIRECTION"], row["ROUTE_ID"])
                  data.append(row)
              except ValueError as e:
                  print(f"Skipping row due to error: {row} - {e}")
  return data

def populateDepartureLoad(data):
  departure_load = 0  # Initial load at the start of the route
  for row in data:
    boardings = int(row['BOARDINGS']) if row['BOARDINGS'] else 0
    alightings = int(row['ALIGHTINGS']) if row['ALIGHTINGS'] else 0
    
    if int(row['STOP_ORDER_NBR']) == 0:
       departure_load = boardings
    else:
       departure_load += boardings - alightings
    row['DEPARTURE_LOAD'] = departure_load

    # with open("departureLoadTest.csv", mode='a', newline='') as outfile:
    #   writer = csv.DictWriter(outfile, fieldnames=["DATE","ROUTE_ID","DIRECTION","TRIP_ID","VEHICLE_ID","SCHEDULED_TIME","ACTUAL_ARRIVAL_TIME","ACTUAL_DEPARTURE_TIME","STOP_ORDER_NUMBER","STOP_ID","STOP_NAME","BOARDINGS","ALIGHTINGS", "DAY_TYPE", "TIME_PERIOD", "DEPARTURE_LOAD"])
    #   writer.writerow(row)

  return data

def aggregateBoardingAndAlightingData(serviceChange, data):
  #dataSchema = OPERATION_DATE,ROUTE_ID,DIRECTION,TRIP_ID,VEHICLE_ID,SCHED_DEPTIME,ACT_ARRTIME,ACT_DEPTIME,STOP_ORDER_NBR,STOP_ID,STOP,BOARDINGS,ALIGHTINGS

  # Aggregate data
  aggregated_data = defaultdict(lambda: {"total_alightings": 0, "total_boardings": 0, "total_departure_load": 0, "trip_counts": [], "date_totals": defaultdict(int)})
  unique_dates = {"Weekday": set(), "Saturday": set(), "Sunday": set()}

  for row in data:
      key = (row["ROUTE_ID"], row["DIRECTION"], row["TIME_PERIOD"], row["STOP_ID"], row["STOP"], row["DAY_TYPE"], row['STOP_ORDER_NBR'])
      aggregated_data[key]["total_alightings"] += row["ALIGHTINGS"]
      aggregated_data[key]["total_boardings"] += row["BOARDINGS"]
      aggregated_data[key]["total_departure_load"] += row["DEPARTURE_LOAD"]
      aggregated_data[key]["trip_counts"].append(row["TRIP_ID"])
      aggregated_data[key]["date_totals"][row["DATE"]] += row["ALIGHTINGS"]
      unique_dates[row["DAY_TYPE"]].add(row["DATE"])

  # Compute averages and departing loads
  output_data = []
  trip_loads = defaultdict(lambda: defaultdict(int))  # { (route, direction, day_type, trip_id) -> { stop_id -> departing_load } }

  for key, values in aggregated_data.items():
      route, direction, time_period, stop_id, stop_name, day_type, stop_order_number = key
      if day_type != "Weekday":
        continue
      num_days = len(unique_dates[day_type])
      num_unique_trips = len(values["trip_counts"])
      
      if num_days > 0 and num_unique_trips > 0:
          avg_total_alightings = values["total_alightings"] / num_days
          avg_trip_alightings = values["total_alightings"] / (num_unique_trips)
          avg_total_boardings = values["total_boardings"] / num_days
          avg_trip_boardings = values["total_boardings"] / (num_unique_trips)
          avg_trip_departing_load = values["total_departure_load"] / (num_unique_trips)

          output_data.append({
              "serviceChangeNum": serviceChange,
              "routeNum": route,
              "direction": direction,
              "stopId": stop_id,
              "stopName": stop_name,
              "stopOrderNum": stop_order_number,
              "timeOfDay": time_period,
              "tripBoardings": f"{avg_trip_boardings:.3f}",
              "tripAlightings": f"{avg_trip_alightings:.3f}",
              "departingLoad": f"{avg_trip_departing_load:.3f}",
              "dailyBoardings": f"{avg_total_boardings:.3f}",
              "dailyAlightings": f"{avg_total_alightings:.3f}"
          })
  return output_data

def writeOutput(outputData, routeId, serviceChange):
  
  directory = f"../../data/routeData/ct/{routeId}/{serviceChange}"
  if routeId[0] == "5" and len(routeId) == 3:
    print(f"st route: {routeId}")
    directory = f"../../data/routeData/st/{routeId}/{serviceChange}"
  
  os.makedirs(directory, exist_ok=True)

  # Write results to CSV, only weekday. 
  fileName = os.path.join(directory, 'ridershipData.csv')

  with open(fileName, "w", newline="") as file:
      fieldnames = ['serviceChangeNum', 'routeNum', 'direction', 'stopId', 'stopName', 'stopOrderNum', 'timeOfDay', 'tripBoardings', 'tripAlightings', 'departingLoad', 'dailyBoardings', 'dailyAlightings']
      writer = csv.DictWriter(file, fieldnames=fieldnames)
      writer.writeheader()
      writer.writerows(outputData)

  print(f"Output written to {fileName}")

def runAggregationForRoute(routeId, month, year):
  serviceChange = year[2:]+month
  print(serviceChange)
  fullFilePath = "../../data/rawData/ct/ctDataByRoute/{0}/{1}/{2}/routeData.csv".format(routeId, year, month) 
  print(fullFilePath)
  inputData = get_input_data(fullFilePath)
  print(inputData[1])
  dataWithDepartureLoads = populateDepartureLoad(inputData)
  print(dataWithDepartureLoads[1])
  aggregatedData = aggregateBoardingAndAlightingData(serviceChange, dataWithDepartureLoads)
  writeOutput(aggregatedData, routeId, serviceChange)


#Edit these
routeIds = ["101"]
years = ["2023", "2024", "2025"]
months = ["10"]

#for routeId in routeIds:
for i in range(100, 1000):
  routeId = str(i)
  for year in years:
    for month in months:
      try:
        print("{0} from {1}/{2}".format(routeId, month, year))
        runAggregationForRoute(routeId, month, year)
      except:
        print("route {0} from {1}/{2} DNE".format(routeId, month, year))
        continue

#outputRow = {"serviceChangeNum": row['SERVICE_CHANGE_NUM'],
                      #  "routeNum": row['SERVICE_RTE_NUM'],
                      #  "direction": row['INBD_OUTBD_CD'],
                      #  "stopId": row['STOP_ID'],
                      #  "stopName": stopName,
                      #  "stopOrderNum": row['STOP_SEQUENCE_NUM'],
                      #  "timeOfDay": row['DAY_PART_CD'],
                      #  "tripBoardings": row['AVG_TRIP_BOARDINGS'],
                      #  "tripAlightings": row['AVG_TRIP_ALIGHTINGS'],
                      #  "departingLoad": row['AVG_TRIP_DEPARTING_LOAD'],
                      #  "dailyBoardings": row['AVG_TOTAL_BOARDINGS'],
                      # "dailyAlightings": row['AVG_TOTAL_ALIGHTINGS']
                      #  }
