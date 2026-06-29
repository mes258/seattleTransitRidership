import pandas as pd
import os
#rawDataFilePath = "../../data/rawData/ct/Stop_Activity_ST.xlsx"
rawDataFilePath = "../../data/rawData/ct/Stop_Activity_CT.xlsx"

# st: 3 sheets, ct: 6 sheets. 
excelSheetNum = 0
isValidExcelSheet = True
while (isValidExcelSheet):
  # OPERATION_DATE  ROUTE_ID DIRECTION  TRIP_ID  VEHICLE_ID SCHED_DEPTIME ACT_ARRTIME ACT_DEPTIME  STOP_ORDER_NBR  STOP_ID  STOP  BOARDINGS  ALIGHTINGS
  try:
    print("reading page {0}".format(excelSheetNum))
    df = pd.read_excel(rawDataFilePath, sheet_name=excelSheetNum)
    # Ensure OPERATION_DATE is datetime
    df["OPERATION_DATE"] = pd.to_datetime(df["OPERATION_DATE"])

    # Group by route and date
    grouped = df.groupby(["ROUTE_ID", "OPERATION_DATE"])
    print("got the groups")
    for (routeId, operationDate), group in grouped:
      year = operationDate.strftime("%Y")
      month = operationDate.strftime("%m")
      
      # Build directory path: output/<route>/<year>/<month>/
      dir_path = os.path.join("../../data/rawData/ct/ctDataByRoute", str(routeId), year, month)
      os.makedirs(dir_path, exist_ok=True)
      
      # Output file path
      file_path = os.path.join(dir_path, "routeData.csv")
      
      # If file exists, append; otherwise write with header
      if os.path.exists(file_path):
          group.to_csv(file_path, mode='a', header=False, index=False)
      else:
          group.to_csv(file_path, header=True, index=False)

    excelSheetNum += 1
  except:
    isValidExcelSheet = False


# df = pd.read_excel(rawDataFilePath, sheet_name=8)
# print(df.count())
# print(df.head(10))
# print(df.dtypes)