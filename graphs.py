import matplotlib.pyplot as plt
import plotly
import plotly.express as px
import pandas as pd

def CreatePriorityBar(data):
    priority_list = []
    for line in data:
        priority_list.append(line.priority)
    priority_df = pd.DataFrame(priority_list)
    priority_df.rename(columns={0: "priority"}, inplace=True)
    priority_df = priority_df.priority.value_counts()
    fig = px.bar(
        x=priority_df.index,
        y=priority_df.values,
        labels=priority_df.index,
        color=priority_df.values,
        color_continuous_scale=px.colors.sequential.Blugrn,
        height=350
    )

    fig.update_layout(
        xaxis_title="Priority (10 being urgent)",
        yaxis_title="Number of Projects",
        xaxis_range=[1, 10],
        yaxis_range=[1, 10],
        coloraxis_showscale=False,
    )

    fig.update_xaxes(dtick=1)
    fig.update_yaxes(dtick=1)

    fig.write_image("static/images/priority_bar.png")


def CreateTimeBar(data):
    time_list = []
    for line in data:
        time_list.append(line.time_to_fix)
    time_df = pd.DataFrame(time_list)
    time_df.rename(columns={0: "time"}, inplace=True)
    time_df = time_df.time.value_counts()
    fig = px.bar(
        x=time_df.index,
        y=time_df.values,
        labels=time_df.index,
        color=time_df.values,
        color_continuous_scale=px.colors.sequential.Redor,
        height=350
    )

    fig.update_layout(
        xaxis_title="Time to Complete (10 being very long)",
        yaxis_title="Number of Projects",
        xaxis_range=[1, 10],
        yaxis_range=[1, 10],
        coloraxis_showscale=False
    )

    fig.update_xaxes(dtick=1)
    fig.update_yaxes(dtick=1)

    fig.write_image("static/images/time_bar.png")


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
        legend=dict(font=dict(size=20))
    )

    fig.write_image("static/images/pie_chart.png")

