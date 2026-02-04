import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go

from .config import timePeriodNames

timeOfDay = ["AM", "MID", "PM", "XEV", "XNT"]

timeColors = {
    "XNT": "#000000",
    "XEV": "#af2db9",
    "PM":  "#377d22",
    "AM":  "#bfbe3c",
    "MID": "#0023f5",
}

# These offsets are used to align multiple bars at the same y value.
yOffsetsInbound = {
    "AM":  -0.3,
    "MID": -0.15,
    "PM":   0.00,
    "XEV": +0.15,
    "XNT": +0.3,
}

yOffsetsOutbound = {
    "AM":  +0.3,
    "MID": +0.15,
    "PM":   0.00,
    "XEV": -0.15,
    "XNT": -0.3,
}

legendLabels = {
    "AM":  "5am-9am (AM)",
    "MID": "9am-3pm (MID)",
    "PM":  "3pm-7pm (PM)",
    "XEV": "7pm-10pm (XEV)",
    "XNT": "10pm-5am (XNT)",
}

# Add all named routes here, regardless of agency.
# TODO: consolidate all of the route mappings into one place
namedRouteMappings = {
  "671": "A Line",
  "672": "B Line",
  "673": "C Line",
  "674": "D Line",
  "675": "E Line",
  "676": "F Line",
  "677": "G Line",
  "678": "H Line"
}

def plotTripRidership(df, routeNum, timePeriod):
    fig = make_subplots(
        rows=1,
        cols=2,
        shared_yaxes=False,
        horizontal_spacing=0.25,
        subplot_titles=("Inbound (Read Down)", "Outbound (Read Up)"),
    )

    # Compute x-axis range across both plots
    max_x = max(
        df["tripBoardings"].max(),
        df["departingLoad"].max(),
    )
    min_x = df["tripAlightings"].max()

    x_range = [-min_x * 1.1, max_x * 1.1]

    for col, direction in enumerate(["I", "O"], start=1):
        dfd = df[df["direction"] == direction].copy()

        # Y axis index: 
        stops = (
            dfd[["stopOrderNum", "stopName"]]
            .drop_duplicates()
            .sort_values("stopOrderNum")
            .reset_index(drop=True)
        )
        stops["y_pos"] = range(len(stops))

        dfd = dfd.merge(
            stops[["stopOrderNum", "y_pos"]],
            on="stopOrderNum",
            how="left",
        )

        dfd["base_y"] = dfd["y_pos"]

        # One legend per plot
        legend_shown = set()

        for tod in timeOfDay:
            dft = dfd[dfd["timeOfDay"] == tod]

            show_legend = tod not in legend_shown

            if direction == "I":
              y_vals = dft["base_y"] + yOffsetsInbound[tod]
            else:
              y_vals = dft["base_y"] + yOffsetsOutbound[tod]

            # Boarding data
            if direction == "I": # Inbound
              fig.add_trace(
                  go.Bar(
                      x=dft["tripBoardings"],
                      y=y_vals,
                      orientation="h",
                      marker_color=timeColors[tod],
                      opacity=1,
                      name=legendLabels[tod],
                      legendgroup=tod,
                      showlegend=show_legend, # Add legend if needed
                      hovertemplate="Boardings: %{x}<extra></extra>",
                      width=0.15
                  ),
                  row=1,
                  col=col,
              )
            else: # Outbound
              fig.add_trace(
                go.Bar(
                    x=dft["tripBoardings"],
                    y=y_vals,
                    orientation="h",
                    marker_color=timeColors[tod],
                    opacity=1,
                    name=legendLabels[tod],
                    legendgroup=tod,
                    showlegend=False,
                    hovertemplate="Boardings: %{x}<extra></extra>",
                    width=0.15
                ),
                row=1,
                col=col,
            )

            # Alighting Data
            fig.add_trace(
                go.Bar(
                    x=-dft["tripAlightings"],
                    y=y_vals,
                    orientation="h",
                    marker_color=timeColors[tod],
                    opacity=1,
                    legendgroup=tod,
                    showlegend=False,
                    hovertemplate="Alightings: %{x}<extra></extra>",
                    width=0.15
                ),
                row=1,
                col=col,
            )

            # Departing load data
            fig.add_trace(
                go.Scatter(
                    x=dft["departingLoad"],
                    y=y_vals,
                    mode="markers",
                    marker=dict(
                        size=4,
                        color=timeColors[tod],
                        #line=dict(width=0.15, color="black"),
                    ),
                    name=f"{tod.upper()} load",
                    legendgroup=tod,
                    showlegend=False,
                    hovertemplate="Passengers on board: %{x}<extra></extra>",
                ),
                row=1,
                col=col,
            )

            if show_legend:
              legend_shown.add(tod)

        y_min = -0.5
        y_max = len(stops) - 0.5

        # Y axis formatting
        fig.update_yaxes(
            tickvals=stops["y_pos"],
            ticktext=stops["stopName"],
            range=[y_min, y_max],
            autorange="reversed" if direction == "I" else False,
            row=1,
            col=col,
        )

        # X axis formatting
        fig.update_xaxes(
            range=x_range,
            zeroline=True,
            zerolinewidth=1,
            zerolinecolor="black",
            row=1,
            col=col,
        )

    if routeNum in namedRouteMappings:
       routeName = namedRouteMappings[routeNum]
    else:
       routeName = f"Route {routeNum}"

    seasonYear = timePeriodNames[timePeriod]
    title = f"Average Weekday Ridership per {routeName} Trip in {seasonYear}"
    fig.update_layout(
        barmode="overlay",
        title=title,
        height=800,
        bargap=0.25,
        legend_title_text="Time Period",
        template="plotly_white",
    )

    #fig.show()

    return fig.to_json()

def plotDailyRidership(df, routeNum, timePeriod):
    fig = make_subplots(
        rows=1,
        cols=2,
        shared_yaxes=False,
        horizontal_spacing=0.25,
        subplot_titles=("Inbound (Read Down)", "Outbound (Read Up)"),
    )

    # Compute x-axis range across both plots
    stop_totals = (
      df.groupby(["direction", "stopOrderNum"])
        .agg(
            total_boardings=("dailyBoardings", "sum"),
            total_alightings=("dailyAlightings", "sum"),
        )
        .reset_index()
    )

    max_x = max(
        stop_totals["total_boardings"].max(),
        stop_totals["total_alightings"].max(),
    )

    x_range = [-max_x * 1.1, max_x * 1.1]

    legend_shown = set()

    for col, direction in enumerate(["I", "O"], start=1):
        dfd = df[df["direction"] == direction].copy()

        # Y axis index: 
        stops = (
            dfd[["stopOrderNum", "stopName"]]
            .drop_duplicates()
            .sort_values("stopOrderNum")
            .reset_index(drop=True)
        )
        stops["y_pos"] = range(len(stops))

        dfd = dfd.merge(
            stops[["stopOrderNum", "y_pos"]],
            on="stopOrderNum",
            how="left",
        )

        for tod in timeOfDay:
            dft = dfd[dfd["timeOfDay"] == tod]
            if dft.empty:
                continue

            show_legend = tod not in legend_shown

            # Boarding data
            fig.add_trace(
                go.Bar(
                    x=dft["dailyBoardings"],
                    y=dft["y_pos"],
                    orientation="h",
                    marker_color=timeColors[tod],
                    name=legendLabels[tod],
                    legendgroup=tod,
                    showlegend=show_legend,
                    hovertemplate="Boardings: %{x}<extra></extra>",
                ),
                row=1,
                col=col,
            )

            # Alighting data
            fig.add_trace(
                go.Bar(
                    x=-dft["dailyAlightings"],
                    y=dft["y_pos"],
                    orientation="h",
                    marker_color=timeColors[tod],
                    legendgroup=tod,
                    showlegend=False,
                    hovertemplate="Alightings: %{x}<extra></extra>",
                ),
                row=1,
                col=col,
            )

            if show_legend:
                legend_shown.add(tod)

        y_min = -0.5
        y_max = len(stops) - 0.5

        # Y axis formatting
        fig.update_yaxes(
            tickvals=stops["y_pos"],
            ticktext=stops["stopName"],
            range=[y_min, y_max],
            autorange="reversed" if direction == "I" else False,
            side="left",
            row=1,
            col=col,
        )

        # X axis formatting
        fig.update_xaxes(
            range=x_range,
            zeroline=True,
            zerolinewidth=1,
            zerolinecolor="black",
            row=1,
            col=col,
        )

    if routeNum in namedRouteMappings:
        routeName = namedRouteMappings[routeNum]
    else:
        routeName = f"Route {routeNum}"

    seasonYear = timePeriodNames[timePeriod]
    title = f"Average Daily Stop Ridership for {routeName} in {seasonYear}"

    fig.update_layout(
        barmode="relative",
        title=title,
        height=800,
        legend_title_text="Time Period",
        template="plotly_white",
    )

    #fig.show()
    return fig.to_json()

# Test Plots
# routeNum = "675"
# timePeriod = "243"
# dfToPlot = am.getRidershipData("kcm", routeNum, timePeriod)
# print(plotDailyRidership(dfToPlot, routeNum, timePeriod))
# print(plotTripRidership(dfToPlot, routeNum, timePeriod))