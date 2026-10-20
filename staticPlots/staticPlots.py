import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Patch
import os

namedRouteMappings = {
  ("blue", "701", "Swift Blue Line"),
  ("green", "702", "Swift Green Line"),
  ("orange", "703", "Swift Orange Line"),
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
  "253": "Aug 30, 2025 - Mar 27, 2026",
  "261": "Mar 28, 2026 - Aug 28, 2026",
  "2310": "October 2023",
  "2410": "October 2024",
  "2510": "October 2025"
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

    #print(inbound_df.count())

    # ---------------------------
    # BUILD DICTIONARY STRUCTURE
    # ---------------------------
    def build_direction_dict(direction_df, shouldReverse):

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
            ]["stopOrderNum"].iloc[0], 
            reverse=shouldReverse
        )

        return dict(ordered)

    inbound_sorted_data = build_direction_dict(inbound_df, True)
    outbound_sorted_data = build_direction_dict(outbound_df, False)

    #print(outbound_sorted_data)

    # ---------------------------
    # TITLES
    # ---------------------------
    # Before setting up the plot, create all the labels: 
    routeName = "Route {0}".format(route_number)
    for letter, rapidRideRouteNum, shortName in namedRouteMappings:
      if route_number == rapidRideRouteNum:
        routeName = shortName

    timeSpanModifier = "between"
    if len(service_change) == 4:
        timeSpanModifier = "in"
    overallTitle = "Average Weekday Ridership per {0} Trip {1} {2}".format(routeName, timeSpanModifier, timePeriodNames[service_change])
    inboundTitle = "Inbound Trips"
    outboundTitle = "Outbound Trips"
    inboundYAxis = "{0} Inbound Stops (Read Down)".format(routeName)
    outboundYAxis = "{0} Outbound Stops (Read Up)".format(routeName)
    xAxis = "Passenger Count"

    mainTitleSize = 40
    subTitleSize = 30
    axisLabelSizeValue = min(getAxisLabelSize(len(inbound_sorted_data), len(outbound_sorted_data)), 20)
    print(f"axis label size: {axisLabelSizeValue}")
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

    for i in range(len(time_periods)):
        ax1.barh(0, 0, color=time_order_color[i][1], label=time_order_color[i][0])
        ax2.barh(0, 0, color=time_order_color[i][1], label=time_order_color[i][0])
    ax1.legend()
    ax2.legend()

    # ---------------------------
    # SAVE OUTPUT
    # ---------------------------
    directory = f"../STR/{agency}/{route_number}/{service_change}"
    os.makedirs(directory, exist_ok=True)

    output_file = os.path.join(directory, "TripRidership.png")
    fig.savefig(output_file)
    plt.close(fig)

    #plt.show()

# plot_trip_ridership_from_csv("../data/routeData/st/48/253/ridershipData.csv", "kcm", "48", "253")

def plot_daily_ridership_from_csv(csv_path, agency, route_number, service_change):
    
    df = pd.read_csv(csv_path)

    if df.empty:
        raise ValueError("No data found for given route and service change.")

    df = df.sort_values(by=["direction", "stopOrderNum"])

    time_periods = ["AM", "MID", "PM", "XEV", "XNT"]

    # ---------------------------
    # BUILD DATA STRUCTURE
    # ---------------------------
    def build_direction_dict(direction_df, shouldReverse):

        direction_dict = {}
        grouped = direction_df.groupby(["stopId", "stopName"])

        for (stop_id, stop_name), group in grouped:
            group = group.sort_values("stopOrderNum")
            values = []

            for t in time_periods:
                row = group[group["timeOfDay"] == t]

                if row.empty:
                    values.append((0, 0))
                else:
                    row = row.iloc[0]
                    neg_bar = row["dailyAlightings"]
                    pos_bar = row["dailyBoardings"]
                    values.append((neg_bar, pos_bar))

            direction_dict[(stop_id, stop_name)] = values

        # Preserve stop order
        ordered = sorted(
            direction_dict.items(),
            key=lambda x: direction_df[
                direction_df["stopId"] == x[0][0]
            ]["stopOrderNum"].iloc[0], 
            reverse=shouldReverse
        )

        return dict(ordered)

    inbound_df = df[df["direction"] == "I"]
    outbound_df = df[df["direction"] == "O"]

    inbound_sorted_data = build_direction_dict(inbound_df, True)
    outbound_sorted_data = build_direction_dict(outbound_df, False)

    # ---------------------------
    # TITLES
    # ---------------------------
    routeName = "Route {0}".format(route_number)
    for letter, rapidRideRouteNum, shortName in namedRouteMappings:
      if route_number == rapidRideRouteNum:
        routeName = shortName

    timeSpanModifier = "between"
    if len(service_change) == 4:
        timeSpanModifier = "in"
    overallTitle = "Average Daily Stop Ridership for {0} {1} {2}".format(routeName, timeSpanModifier, timePeriodNames[service_change])
    inboundTitle = "Inbound Trips"
    outboundTitle = "Outbound Trips"
    inboundYAxis = "{0} Inbound Stops (Read Down)".format(routeName)
    outboundYAxis = "{0} Outbound Stops (Read Up)".format(routeName)
    xAxis = "Passenger Count"

    mainTitleSize = 40
    subTitleSize = 30
    axisLabelSizeValue = min(getAxisLabelSize(len(inbound_sorted_data), len(outbound_sorted_data)), 20)
    print(f"axis label size: {axisLabelSizeValue}")
    axisLabelSize = axisLabelSizeValue 
    axisIncrementsSize = axisLabelSizeValue
    legendTextSize = 15

    # ---------------------------
    # FIGURE
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

    time_colors = ['y', 'b', 'g', 'm', 'k']

    max_pos = 0
    max_neg = 0

    def plot_direction(ax, data_dict):
        nonlocal max_pos, max_neg

        for i, ((stop_id, stop_name), values) in enumerate(data_dict.items()):
            neg_offset = 0
            pos_offset = 0

            for j, (alight, board) in enumerate(values):
                # stack alightings (negative)
                ax.barh(i, -alight, left=neg_offset, color=time_colors[j], height=0.6)
                neg_offset -= alight

                # stack boardings (positive)
                ax.barh(i, board, left=pos_offset, color=time_colors[j], height=0.6)
                pos_offset += board

            max_pos = max(max_pos, pos_offset)
            max_neg = min(max_neg, neg_offset)

        # labels
        stop_labels = [stop_name for (_, stop_name) in data_dict.keys()]
        ax.set_yticks(range(len(stop_labels)))
        ax.set_yticklabels(stop_labels)

    plot_direction(ax1, inbound_sorted_data)
    plot_direction(ax2, outbound_sorted_data)

    # axis limits
    ax1.set_xlim(max_neg * 1.1, max_pos * 1.1)
    ax2.set_xlim(max_neg * 1.1, max_pos * 1.1)

    # legend
    time_order_color = [
        ['5am-9am (AM)', 'y'],
        ['9am-3pm (MID)', 'b'],
        ['3pm-7pm (PM)', 'g'],
        ['7pm-10pm (XEV)', 'm'],
        ['10pm-5am (XNT)', 'k']
    ]

    for i in range(len(time_periods)):
        ax1.barh(0, 0, color=time_order_color[i][1], label=time_order_color[i][0])
        ax2.barh(0, 0, color=time_order_color[i][1], label=time_order_color[i][0])
    ax1.legend()
    ax2.legend()
    

    plt.tight_layout(rect=[0, 0, 1, 0.95])


    # ---------------------------
    # SAVE
    # ---------------------------
    directory = f"../STR/{agency}/{route_number}/{service_change}"
    os.makedirs(directory, exist_ok=True)

    output_file = os.path.join(directory, "DailyRidership.png")

    fig.savefig(output_file, dpi=200)
    plt.close(fig)

def plot_daily_ridership_comparison_from_csv(
    csv_path_1, csv_path_2, agency, route_number, service_change_1, service_change_2
):
    """Save adjacent daily ridership stacks for two route CSVs and return the path.

    Each CSV should contain one route and service change, as for
    plot_daily_ridership_from_csv. Within each direction, equal-length stop
    sequences are matched by position in stopOrderNum order, using the second
    service change's names. Otherwise, stops are matched by stopId, using the
    second change's names and order where shared. Stops present in only one
    change retain an empty slot for the other.
    The first change is faded; boardings extend right and alightings left.
    Output is ../STR/{agency}/{route}/{change_1}_vs_{change_2}/DailyRidership.png.
    """
    frames = [pd.read_csv(csv_path_1), pd.read_csv(csv_path_2)]
    if any(df.empty for df in frames):
        raise ValueError("No data found for given route and service change.")

    periods = ["AM", "MID", "PM", "XEV", "XNT"]
    period_labels = ["5am-9am (AM)", "9am-3pm (MID)", "3pm-7pm (PM)",
                     "7pm-10pm (XEV)", "10pm-5am (XNT)"]
    colors = ['y', 'b', 'g', 'm', 'k']
    changes = [str(service_change_1), str(service_change_2)]
    change_labels = [timePeriodNames.get(change, change) for change in changes]
    route_name = f"Route {route_number}"
    for letter, route_num, short_name in namedRouteMappings:
        if str(route_number) == route_num:
            route_name = short_name

    direction_data = []
    for direction in ["I", "O"]:
        subsets = [df[df["direction"] == direction] for df in frames]
        ordered_stops = [
            subset.sort_values("stopOrderNum", kind="stable").drop_duplicates("stopId")
            for subset in subsets
        ]
        if len(ordered_stops[0]) == len(ordered_stops[1]):
            stop_mapping = dict(zip(
                ordered_stops[0]["stopId"], ordered_stops[1]["stopId"]
            ))
            subsets[0] = subsets[0].copy()
            subsets[0]["stopId"] = subsets[0]["stopId"].map(stop_mapping)
        stops = (
            pd.concat([subsets[1], subsets[0]])
            .drop_duplicates("stopId")
            .sort_values("stopOrderNum", ascending=direction == "O", kind="stable")
        )
        totals = [
            subset.groupby(["stopId", "timeOfDay"])[
                ["dailyAlightings", "dailyBoardings"]
            ].sum()
            for subset in subsets
        ]
        direction_data.append((stops, totals))

    label_size = max(6, min(getAxisLabelSize(
        len(direction_data[0][0]), len(direction_data[1][0])
    ), 20))
    legend_handles = [
        Patch(facecolor=color, alpha=alpha, label=f"{change_label} {period_label}")
        for period_label, color in zip(period_labels, colors)
        for change_label, alpha in zip(change_labels, [0.5, 1.0])
    ]
    fig, axes = plt.subplots(1, 2, figsize=(30, 20), constrained_layout=True)
    try:
        fig.suptitle(
            f"Average Daily Stop Ridership for {route_name}\n"
            f"{change_labels[0]} and {change_labels[1]}",
            fontsize=40,
        )
        max_boardings = 0
        max_alightings = 0
        for ax, direction, (stops, totals) in zip(
            axes, ["Inbound", "Outbound"], direction_data
        ):
            for i, stop_id in enumerate(stops["stopId"]):
                for values, offset, alpha in zip(totals, [0.15, -0.15], [0.5, 1.0]):
                    boardings = 0
                    alightings = 0
                    for period, color in zip(periods, colors):
                        if (stop_id, period) not in values.index:
                            continue
                        alight, board = values.loc[stop_id, period]
                        ax.barh(i + offset, -alight, left=-alightings,
                                color=color, alpha=alpha, height=0.3)
                        ax.barh(i + offset, board, left=boardings,
                                color=color, alpha=alpha, height=0.3)
                        alightings += alight
                        boardings += board
                    max_boardings = max(max_boardings, boardings)
                    max_alightings = max(max_alightings, alightings)

            ax.set_yticks(range(len(stops)))
            ax.set_yticklabels(stops["stopName"])
            ax.set_title(f"{direction} Trips", fontsize=30)
            ax.set_xlabel("Passenger Count", fontsize=label_size)
            reading_order = "Down" if direction == "Inbound" else "Up"
            ax.set_ylabel(
                f"{route_name} {direction} Stops (Read {reading_order})",
                fontsize=label_size,
            )
            ax.tick_params(axis="both", labelsize=label_size)
            ax.grid(True)
            ax.set_axisbelow(True)
            ax.legend(handles=legend_handles)

        for ax in axes:
            ax.set_xlim(-max(max_alightings * 1.1, 1), max(max_boardings * 1.1, 1))

        directory = f"../STR/{agency}/{route_number}/{changes[0]}_vs_{changes[1]}"
        os.makedirs(directory, exist_ok=True)
        output_file = os.path.join(directory, "DailyRidership.png")
        fig.savefig(output_file, dpi=200)
        return output_file
    finally:
        plt.close(fig)



# Uncomment this to generate the plots for all Metro routes (also, change the service change below)
for routeInt in range(1000):
  print(routeInt)
  try:
    plot_trip_ridership_from_csv(f"../data/routeData/kcm/{routeInt}/261/ridershipData.csv", "kcm", f"{routeInt}", "261")
    plot_daily_ridership_from_csv(f"../data/routeData/kcm/{routeInt}/261/ridershipData.csv", "kcm", f"{routeInt}", "261")

    # plot_trip_ridership_from_csv(f"../data/routeData/kcm/{routeInt}/253/ridershipData.csv", "kcm", f"{routeInt}", "253")
    # plot_daily_ridership_from_csv(f"../data/routeData/kcm/{routeInt}/253/ridershipData.csv", "kcm", f"{routeInt}", "253")
  except:
      continue

#Uncomment this to generate the plots for all Sound Transit routes (also, change the service change below)
for routeInt in range(500, 600):
  print(routeInt)
  try:
    plot_trip_ridership_from_csv(f"../data/routeData/st/{routeInt}/261/ridershipData.csv", "st", f"{routeInt}", "261")
    plot_daily_ridership_from_csv(f"../data/routeData/st/{routeInt}/261/ridershipData.csv", "st", f"{routeInt}", "261")

    # plot_trip_ridership_from_csv(f"../data/routeData/st/{routeInt}/253/ridershipData.csv", "st", f"{routeInt}", "253")
    # plot_daily_ridership_from_csv(f"../data/routeData/st/{routeInt}/253/ridershipData.csv", "st", f"{routeInt}", "253")
  except:
      continue

# Uncomment this to generate the plots for all Community Transit routes (also, change the service change below)
# for routeInt in range(99, 1000):
#   print(routeInt)
#   try:
#     plot_trip_ridership_from_csv(f"../data/routeData/ct/{routeInt}/2310/ridershipData.csv", "ct", f"{routeInt}", "2310")
#     plot_daily_ridership_from_csv(f"../data/routeData/ct/{routeInt}/2310/ridershipData.csv", "ct", f"{routeInt}", "2310")
#   except:
#     print("no 2023 data")

#   try:
#     plot_trip_ridership_from_csv(f"../data/routeData/ct/{routeInt}/2410/ridershipData.csv", "ct", f"{routeInt}", "2410")
#     plot_daily_ridership_from_csv(f"../data/routeData/ct/{routeInt}/2410/ridershipData.csv", "ct", f"{routeInt}", "2410")
#   except:
#     print("no 2024 data")

#   try:
#     plot_trip_ridership_from_csv(f"../data/routeData/ct/{routeInt}/2510/ridershipData.csv", "ct", f"{routeInt}", "2510")
#     plot_daily_ridership_from_csv(f"../data/routeData/ct/{routeInt}/2510/ridershipData.csv", "ct", f"{routeInt}", "2510")
#   except:
#     print("no 2025 data")

# Uncomment this to generate the plots for all Community Transit operated ST routes (also, change the service change below)
# for routeInt in range(500, 599):
#   print(routeInt)
#   try:
#     plot_trip_ridership_from_csv(f"../data/routeData/st/{routeInt}/2310/ridershipData.csv", "st", f"{routeInt}", "2310")
#     plot_daily_ridership_from_csv(f"../data/routeData/st/{routeInt}/2310/ridershipData.csv", "st", f"{routeInt}", "2310")
#   except:
#     print("no 2023 data")

#   try:
#     plot_trip_ridership_from_csv(f"../data/routeData/st/{routeInt}/2410/ridershipData.csv", "st", f"{routeInt}", "2410")
#     plot_daily_ridership_from_csv(f"../data/routeData/st/{routeInt}/2410/ridershipData.csv", "st", f"{routeInt}", "2410")
#   except:
#     print("no 2024 data")

#   try:
#     plot_trip_ridership_from_csv(f"../data/routeData/st/{routeInt}/2510/ridershipData.csv", "st", f"{routeInt}", "2510")
#     plot_daily_ridership_from_csv(f"../data/routeData/st/{routeInt}/2510/ridershipData.csv", "st", f"{routeInt}", "2510")
#   except:
#     print("no 2025 data")