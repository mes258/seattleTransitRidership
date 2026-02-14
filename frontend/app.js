const agencyMapping = {
  "kcm": 'King County Metro',
  "st": 'Sound Transit',
  "ct": 'Community Transit'
}

const routeMapping = {
  "671": 'A Line',
  "672": 'B Line',
  "673": 'C Line',
  "674": 'D Line',
  "675": 'E Line',
  "676": 'F Line',
  "677": 'G Line',
  "678": 'H Line'
};

const serviceChangeMapping = {
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

document.addEventListener("DOMContentLoaded", () => {
  var agencySelect = document.getElementById("agencySelect");
  var routeSelect = document.getElementById("routeSelect");
  var serviceChangeSelect = document.getElementById("serviceChangeSelect");
  var submitBtn = document.getElementById("submitBtn");

  var tripChartDiv = document.getElementById("tripChart");
  var dailyChartDiv = document.getElementById("dailyChart");

  var routeDataDiv = document.getElementById("routeData");

  function clearSelect(select, placeholder) {
    select.innerHTML = `<option value="">${placeholder}</option>`;
    select.disabled = true;
  }

  function populateSelect(select, values, placeholder, mapping) {
    clearSelect(select, placeholder);
    values.forEach(v => {
      textValue = v
      if (mapping[v] != undefined){
        textValue =  mapping[v]
      }
      // console.log(textValue)

      const opt = document.createElement("option");
      opt.value = v;
      opt.textContent = textValue;
      select.appendChild(opt);
    });
    select.disabled = false;
  }

  fetch("/api/agencies")
    .then(res => res.json())
    .then(agencies => {
      // console.log(agencies)
      populateSelect(agencySelect, agencies, "Select agency…", agencyMapping);
    });

  agencySelect.addEventListener("change", () => {
    const agency = agencySelect.value;

    clearSelect(routeSelect, "Select route…");
    clearSelect(serviceChangeSelect, "Select service change…");
    submitBtn.disabled = true;

    if (!agency) return;

    fetch(`/api/agencies/${agency}/routes`)
      .then(res => res.json())
      .then(routes => {
        // console.log(routes)
        populateSelect(routeSelect, routes, "Select route…", routeMapping);
      });
  });

  routeSelect.addEventListener("change", () => {
    const agency = agencySelect.value;
    const route = routeSelect.value;

    clearSelect(serviceChangeSelect, "Select service change…",);
    submitBtn.disabled = true;

    if (!route) return;

    fetch(`/api/agencies/${agency}/routes/${route}/serviceChanges`)
      .then(res => res.json())
      .then(serviceChanges => {
        populateSelect(serviceChangeSelect, serviceChanges, "Select service change…", serviceChangeMapping);
      });
  });

  serviceChangeSelect.addEventListener("change", () => {
    submitBtn.disabled = !serviceChangeSelect.value;
  });

  submitBtn.addEventListener("click", () => {
    const agency = agencySelect.value;
    const route = routeSelect.value;
    const serviceChange = serviceChangeSelect.value;

    submitBtn.disabled = true;
    // Fix the issues ehre. 
    fetch(`/api/ridershipCharts?agency=${agency}&route=${route}&serviceChange=${serviceChange}`)
      .then(res => res.json())
      .then(data => {

        Plotly.react(
          tripChartDiv,
          data.tripPlotJson.data,
          data.tripPlotJson.layout
        );

        Plotly.react(
          dailyChartDiv,
          data.dailyPlotJson.data,
          data.dailyPlotJson.layout
        );

        // Update route data
        var routeData = data.routeDataJson
        console.log(routeData)
        routeDataDiv.innerHTML = `<h1>${routeData["routeName"]}</h1>`
        routeDataDiv.innerHTML += `<h3>${routeData["destinations"]}</h3>`
        routeDataDiv.innerHTML += `<p>In ${serviceChangeMapping[serviceChange]}, ${agencyMapping[agency]} ${routeData["routeName"]} had about ${routeData["avgWeekdayRidership"].toLocaleString("en-US")} average weekday passengers.</p>`
        if(routeData["scheduleUrl"] != ""){
          routeDataDiv.innerHTML += `<p><a href="${routeData["scheduleUrl"]}">${routeData["routeName"]} schedule and map, from ${agencyMapping[agency]}</a></p>`
        }
        if(routeData["stbUrl"] != ""){
          routeDataDiv.innerHTML += `<p><a href="${routeData["stbUrl"]}">Seattle Transit Blog article on ${routeData["routeName"]} Ridership Patterns</a></p>`
        }
      })
      .finally(() => {
        submitBtn.disabled = false;
      });
  });
});