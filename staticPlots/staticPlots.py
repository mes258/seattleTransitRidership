import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

namedRouteMappings = {
  ("blue", "701", "Blue Line"),
  ("green", "702", "Green Line"),
  ("orange", "703", "Orange Line"),
  ("a", "671", "A Line"),
  ("b", "672", "B Line"),
  ("c", "673", "C Line"),
  ("d", "674", "D Line"),
  ("e", "675", "E Line"),
  ("f", "676", "F Line"),
  ("g", "677", "G Line"),
  ("h", "678", "H Line")
}

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

# Set the stop name label size based on the number of stops. 
def getAxisLabelSize(inboundStopCount, outboundStopCount):
    maxStopCount = max(inboundStopCount, outboundStopCount)
    return -0.2 * maxStopCount + 30


def plot_trip_ridership_from_csv(csv_path, agency, route_number, service_change):

    # ---------------------------
    # LOAD + FILTER CSV
    # ---------------------------
    df = pd.read_csv(csv_path)

    if df.empty:
        raise ValueError("No data found for given route and service change.")

    df = df.sort_values(by=["direction", "stopOrderNum"])

    inbound_df = df[df["direction"] == "I"]
    outbound_df = df[df["direction"] == "O"]

    time_periods = ["AM", "MID", "PM", "XEV", "XNT"]

    print(inbound_df.count())

    # ---------------------------
    # BUILD DICTIONARY STRUCTURE
    # ---------------------------
    def build_direction_dict(direction_df):

        direction_dict = {}

        grouped = direction_df.groupby(["stopId", "stopName"])

        for (stop_id, stop_name), group in grouped:

            group = group.sort_values("stopOrderNum")
            values = []

            for t in time_periods:
                row = group[group["timeOfDay"] == t]

                if row.empty:
                    values.append((-1, 0, 0))
                else:
                    row = row.iloc[0]
                    dot = row["departingLoad"]
                    neg_bar = row["tripAlightings"]
                    pos_bar = row["tripBoardings"]
                    values.append((dot, neg_bar, pos_bar))

            direction_dict[(stop_id, stop_name)] = values

        # Preserve stop order
        ordered = sorted(
            direction_dict.items(),
            key=lambda x: direction_df[
                direction_df["stopId"] == x[0][0]
            ]["stopOrderNum"].iloc[0]
        )

        return dict(ordered)

    inbound_sorted_data = build_direction_dict(inbound_df)
    outbound_sorted_data = build_direction_dict(outbound_df)

    print(outbound_sorted_data)

    # ---------------------------
    # TITLES
    # ---------------------------
    # Before setting up the plot, create all the labels: 
    routeName = "Route {0}".format(route_number)
    for letter, rapidRideRouteNum, shortName in namedRouteMappings:
      if route_number == rapidRideRouteNum:
        routeName = shortName
    overallTitle = "Average Weekday Ridership per {0} Trip between {1}".format(routeName, timePeriodNames[service_change])
    inboundTitle = "Inbound Trips"
    outboundTitle = "Outbound Trips"
    inboundYAxis = "{0} Inbound Stops (Read Down)".format(routeName)
    outboundYAxis = "{0} Outbound Stops (Read Up)".format(routeName)
    xAxis = "Passenger Count"

    mainTitleSize = 40
    subTitleSize = 30
    axisLabelSizeValue = min(getAxisLabelSize(len(inbound_sorted_data), len(outbound_sorted_data)), 20)
    axisLabelSize = axisLabelSizeValue 
    axisIncrementsSize = axisLabelSizeValue
    legendTextSize = 15

    # ---------------------------
    # FIGURE SETUP
    # ---------------------------
    
    fig, (ax1, ax2) = plt.subplots(nrows=1, ncols=2, figsize=(30, 20), constrained_layout=True)
    fig.subplots_adjust(left=0.28, right=0.95, top=0.92, bottom=0.05, wspace=0.25)
    plt.rc('xtick', labelsize=12)     
    plt.rc('ytick', labelsize=12)
    ax1.set_xlabel(xAxis, fontsize=axisLabelSize)
    ax1.set_ylabel(inboundYAxis, fontsize=axisLabelSize)
    ax1.set_title(inboundTitle, fontsize=subTitleSize)
    ax1.tick_params(axis='x', labelsize=axisIncrementsSize)
    ax1.tick_params(axis='y', labelsize=axisIncrementsSize)

    ax2.set_xlabel(xAxis, fontsize=axisLabelSize)
    ax2.set_ylabel(outboundYAxis, fontsize=axisLabelSize)
    ax2.set_title(outboundTitle, fontsize=subTitleSize)
    ax2.tick_params(axis='x', labelsize=axisIncrementsSize)
    ax2.tick_params(axis='y', labelsize=axisIncrementsSize)

    
    ax1.set_xlim(-10, 30)  # Set x-axis limits
    ax2.set_xlim(-10, 30) # Set x-axis limits
    
    fig.suptitle(overallTitle, fontsize=mainTitleSize)

    ax1.grid(True)
    ax2.grid(True)
    ax1.set_axisbelow(True)
    ax2.set_axisbelow(True)



    time_order_color = [
        ['5am-9am (AM)', 'y'],
        ['9am-3pm (MID)', 'b'],
        ['3pm-7pm (PM)', 'g'],
        ['7pm-10pm (XEV)', 'm'],
        ['10pm-5am (XNT)', 'k']
    ]

    time_offset = np.linspace(-0.3, 0.3, len(time_order_color))

    maxPositive = 0
    maxNegative = 0

    # ---------------------------
    # PLOTTING FUNCTION
    # ---------------------------
    def plot_direction(ax, data_dict):

        nonlocal maxPositive, maxNegative

        for i, ((stop_id, stop_name), values) in enumerate(data_dict.items()):
            for j, (dot, neg_bar, pos_bar) in enumerate(values):

                if dot == -1:
                    continue

                maxPositive = max(maxPositive, dot)
                maxNegative = max(maxNegative, neg_bar)

                y_pos = i + time_offset[j] * -1

                ax.plot(dot, y_pos, 'o' + time_order_color[j][1], markersize=7)
                ax.barh(y_pos, -neg_bar, color=time_order_color[j][1], height=0.15)
                ax.barh(y_pos, pos_bar, color=time_order_color[j][1], height=0.15)

        stop_labels = [stop_name for (_, stop_name) in data_dict.keys()]
        ax.set_yticks(range(len(stop_labels)))
        ax.set_yticklabels(stop_labels)

        ax.grid(True)
        ax.set_axisbelow(True)

    # ---------------------------
    # DRAW BOTH DIRECTIONS
    # ---------------------------
    plot_direction(ax1, inbound_sorted_data)
    plot_direction(ax2, outbound_sorted_data)

    lowerLimit = (maxNegative * 1.1) * -1
    upperLimit = maxPositive * 1.1

    ax1.set_xlim(lowerLimit, upperLimit)
    ax2.set_xlim(lowerLimit, upperLimit)

    plt.tight_layout(rect=[0, 0, 1, 0.95])

    # ---------------------------
    # SAVE OUTPUT
    # ---------------------------
    directory = f"../STR/{agency}/{route_number}/{service_change}"
    os.makedirs(directory, exist_ok=True)

    output_file = os.path.join(directory, "TripRidership.png")
    fig.savefig(output_file)
    plt.show()

plot_trip_ridership_from_csv("../data/routeData/kcm/48/253/ridershipData.csv", "kcm", "48", "253")