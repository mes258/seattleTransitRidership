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
                  date_obj = datetime.strptime(row["OPERATION_DATE"], "%m/%d/%Y").date()
                  row["DATE"] = date_obj
                  row["DAY_TYPE"] = get_day_type(date_obj)
                  row["ALIGHTINGS"] = int(row["ALIGHTINGS"])
                  row["BOARDINGS"] = int(row["BOARDINGS"])
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
    
    if int(row['STOP_ORDER_NUMBER']) == 0:
       departure_load = boardings
    else:
       departure_load += boardings - alightings
    row['DEPARTURE_LOAD'] = departure_load

    # with open("departureLoadTest.csv", mode='a', newline='') as outfile:
    #   writer = csv.DictWriter(outfile, fieldnames=["DATE","ROUTE_ID","DIRECTION","TRIP_ID","VEHICLE_ID","SCHEDULED_TIME","ACTUAL_ARRIVAL_TIME","ACTUAL_DEPARTURE_TIME","STOP_ORDER_NUMBER","STOP_ID","STOP_NAME","BOARDINGS","ALIGHTINGS", "DAY_TYPE", "TIME_PERIOD", "DEPARTURE_LOAD"])
    #   writer.writerow(row)

  return data

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
