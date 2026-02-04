from pathlib import Path

projectRoot = Path(__file__).resolve().parent.parent.parent
dataRoot = projectRoot / "data"

timePeriodNames = {
  "241": "Spring 2024",
  "243": "Fall 2024"
}

rapidRideRouteMapping = {
  "671": 'a-Line',
  "672": 'b-Line',
  "673": 'c-Line',
  "674": 'd-line',
  "675": 'e-Line',
  "676": 'f-Line',
  "677": 'g-Line',
  "678": 'h-Line'
}

stbKcmUrl = {
  "5": "https://seattletransitblog.com/2025/09/29/ridership-patterns-for-king-county-metro-route-5/",
  "7": "https://seattletransitblog.com/2024/10/21/ridership-patterns-for-king-county-metro-route-7/",
  "8": "https://seattletransitblog.com/2024/11/19/ridership-patterns-for-king-county-metro-route-8/",
  "14": "https://seattletransitblog.com/2011/10/29/ridership-patterns-on-route-14/",
  "27": "https://seattletransitblog.com/2011/10/31/ridership-patterns-on-route-27/",
  "36": "https://seattletransitblog.com/2024/12/05/ridership-patterns-for-king-county-metro-route-36/",
  "40": "https://seattletransitblog.com/2024/12/27/ridership-patterns-for-king-county-metro-route-40/",
  "44": "https://seattletransitblog.com/2025/02/13/ridership-patterns-for-king-county-metro-route-44/",
  "50": "https://seattletransitblog.com/2026/01/08/ridership-patterns-for-king-county-metro-route-50/",
  "62": "https://seattletransitblog.com/2025/03/24/ridership-patterns-for-king-county-metro-route-62/",
  "70": "https://seattletransitblog.com/2024/10/07/ridership-patterns-for-king-county-metro-route-70/",
  "75": "https://seattletransitblog.com/2025/10/13/ridership-patterns-for-king-county-metro-route-75/",
  "160": "https://seattletransitblog.com/2025/03/06/ridership-patterns-for-king-county-metro-route-160/",
  "671": "https://seattletransitblog.com/2025/01/20/ridership-patterns-for-rapidride-a-line/",
  "672": "https://seattletransitblog.com/2025/03/21/ridership-patterns-for-rapidride-b-line/",
  "673": "https://seattletransitblog.com/2024/10/15/ridership-patterns-for-rapidride-c-line/",
  "674": "https://seattletransitblog.com/2024/10/28/ridership-patterns-for-rapidride-d-line/",
  "675": "https://seattletransitblog.com/2024/11/22/ridership-patterns-for-rapidride-e-line/",
  "676": "https://seattletransitblog.com/2025/02/24/ridership-patterns-for-rapidride-f-line/",
  "677": "https://seattletransitblog.com/2025/07/17/ridership-patterns-for-rapidride-g-line/",
  "678": "https://seattletransitblog.com/2024/12/17/ridership-patterns-for-rapidride-h-line/",
}