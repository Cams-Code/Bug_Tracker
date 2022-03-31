import matplotlib.pyplot as plt
import plotly
import plotly.express as px
import pandas as pd

def CreateBar(data):
        pass


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
    fig.write_image("static/images/pie_chart.png")

