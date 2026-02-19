from pathlib import Path

projectRoot = Path(__file__).resolve().parent.parent.parent
dataRoot = projectRoot / "data"

timePeriodNames = {
  "191": "Mar 23, 2019 - Jun 14, 2019",
  "192": "Jun 15, 2019 - Sep 20, 2019",
  "193": "Sep 21, 2019 - Mar 20, 2020",
  "201": "Mar 21, 2020 - Jun 12, 2020",
  "202": "Jun 13, 2020 - Sep 18, 2020",
  "203": "Sep 19, 2020 - Mar 19, 2021",
  "211": "Mar 20, 2021 - Jun 11, 2021",
  "212": "Jun 12, 2021 - Oct 1, 2021",
  "213": "Oct 2, 2021 - Mar 18, 2022",
  "221": "Mar 19, 2022 - Jun 10, 2022",
  "222": "Jun 11, 2022 - Sep 16, 2022",
  "223": "Sep 17, 2022 - Mar 17, 2023",
  "231": "Mar 18, 2023 - Jun 9, 2023",
  "232": "Jun 10, 2023 - Sep 1, 2023",
  "233": "Sep 2, 2023 - Mar 29, 2024",
  "241": "Mar 30, 2024 - Sept 13, 2024",
  "243": "Sept 14, 2024 - Mar 28, 2025",
  "251": "Mar 29, 2025 - Aug 29, 2025",
  "253": "Aug 30, 2025 - Mar 27, 2026"
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