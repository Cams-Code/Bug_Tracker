
import plotly.express as px
import pandas as pd


def CreatePriorityBar(data):
    priority_list = []
    for line in data:
        priority_list.append(line.priority)
    priority_list = sorted(priority_list)
    priority_df = pd.DataFrame(priority_list)
    priority_df.rename(columns={0: "priority"}, inplace=True)
    priority_df = priority_df.priority.value_counts()
    print(priority_df.head)

    fig = px.bar(
        x=priority_df.index,
        y=priority_df.values,
        height=500,
    )

    fig.update_layout(
        xaxis_title="<b>Priority (10 being urgent)</b>",
        yaxis_title="<b>Number of Projects</b>",
        xaxis_linecolor="#000000",
        yaxis_linecolor="#000000",
        xaxis_mirror=True,
        yaxis_mirror=True,
        yaxis_gridcolor="gray",
        xaxis_range=[0.5, 10.5],
        yaxis_range=[0, 5],
        xaxis_tickfont_family="Arial Black",
        yaxis_tickfont_family="Arial Black",
        coloraxis_showscale=False,
        paper_bgcolor="#FFF",
        plot_bgcolor="#FFF",
        font_color="#000000",
    )

    fig.update_xaxes(dtick=1)
    fig.update_yaxes(dtick=1)

    fig.update_traces(marker_line_width=2, marker_line_color="black")

    fig.write_html("templates/priority_chart.html")


def CreateTimeBar(data):
    time_list = []
    for line in data:
        time_list.append(line.time_to_fix)
    time_list = sorted(time_list)
    time_df = pd.DataFrame(time_list)
    time_df.rename(columns={0: "time"}, inplace=True)
    time_df = time_df.time.value_counts()
    fig = px.bar(
        x=time_df.index,
        y=time_df.values,
        labels=time_df.index,
        height=500
    )

    fig.update_layout(
        xaxis_title="<b>Time to Complete (10 being very long)</b>",
        yaxis_title="<b>Number of Projects</b>",
        xaxis_linecolor="#000000",
        yaxis_linecolor="#000000",
        xaxis_mirror=True,
        yaxis_mirror=True,
        yaxis_gridcolor="gray",
        xaxis_range=[0.5, 10.5],
        yaxis_range=[0, 5],
        xaxis_tickfont_family="Arial Black",
        yaxis_tickfont_family="Arial Black",
        coloraxis_showscale=False,
        paper_bgcolor="#FFF",
        plot_bgcolor="#FFF",
        font_color="#000000",
    )

    fig.update_xaxes(dtick=1)
    fig.update_yaxes(dtick=1)

    fig.update_traces(marker_line_width=2, marker_line_color="black", marker_color="darkblue")

    fig.write_html("templates/time_chart.html")


def CreatePie(data):
    status_list = []
    for line in data:
        status_list.append(line.status)
    status_df = pd.DataFrame(status_list)
    status_df.rename(columns={0: "status"}, inplace=True)
    status_df = status_df.status.value_counts()
    fig = px.pie(
        labels=status_df.index,
        values=status_df.values,
        names=status_df.index,
        color=status_df.index,
        color_discrete_map={
            "Not Started": "lightcyan",
            "In Progress": "cyan",
            "Completed": "royalblue",
            "To Review": "darkblue"
        }
    )
    fig.update_traces(
        hoverinfo="label+percent", marker=dict(line=dict(color="#000000", width=2))
    )
    fig.update_layout(
        legend=dict(font=dict(size=15))
    )

    fig.write_html("templates/pie_chart.html", auto_open=False)

