# Seattle Transit Ridership

Seattle Transit Ridership is a tool for learning how transit routes in Puget Sound are used. Since 2024, Seattle Transit Blog 
has shared a detailed look into the ridership patterns of various King County Metro, Sound Transit, and Community Transit 
routes. While the Blog will continue to publish these articles, we cannot cover every route. Seattle Transit
Ridership will share the detailed data for every available route. 

## Features
- Interactive ridership charts for most routes
- Historical ridership data (from as far back as 2019)
- Common ridership data schema (and converters for each agency)

## Road Map
There are a few items that we hope to add soon:
- Route maps
- Route destination list
- Monthy ridership data from the agency (when available)
- Support for more agencies (Community Transit, Pierce Transit, and more!)
- Before/After plots to compare a route's ridership between two service changes

Internal TODOs: 
- Consolidate mapping dictionaries
- Function to remove stored plots and route data when needed

## Running the project locally
1. Install the packages listed in backend/requirements.txt. 
2. Navigate to the Backend folder and run: `uvicorn app.app:app --reload`
3. Open your browser to: `http://127.0.0.1:8000/`

## How to add new service change data
1. Copy the raw CSV to `data/rawData/[agency]`.
2. Check if there are any new named routes. If so, update the mappings in:
    - `backend/app/config.py`
    - `backend/app/graphModule.py`
    - `frontend/app.js`
3. Update the service change mappings in:
    - `backend/app/config.py`
    - `frontend/app.js`
4. Update the stop data by adding the latest stop info in `stopData/[agency]` and running `preProcessScripts/[agency]/mergeStopData.py`. 
5. Update `preProcessScripts/[agency]/dataFormatter.py` and run it.
6. Validate the output.

### Project file structure
- data
  - routeData
    - [agency]
      - [routeNum]
        - [service change or year & month]
          - ridershipData.csv
          - dailyRidershipPlot.json
          - tripRidershipPlot.json
          - routeData.json
  - rawData
    - [agency]
      - [full data CSVs]
  - stopData
    - [agency]
        - allStops.txt
          - Aggregated stop data across time periods
        - stops.txt
          - Latest stop data from agency (get KCM stop data from GTFS feed at: https://kingcounty.gov/en/dept/metro/rider-tools/mobile-and-web-apps)
- preProcessScripts
  - [agency]
    - dataFormatter.py
    - mergeStopData.py
- backend
  - app
    - app.py
    - accessModule.py
    - config.py
    - dataIndex.py
    - graphModule.py
    - routeDataModule.py
  - venv
  - requirements.txt
- frontend
  - index.html
  - about.html
  - app.js
  - styles.css
  - favicon.ico
- README.md
- favicon.jpg