import warnings

# Suppress all FutureWarning warnings
warnings.filterwarnings("ignore", category=FutureWarning)

# Suppress UserWarning warnings
warnings.filterwarnings("ignore", category=UserWarning)

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import numpy as np
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

# Import data (Make sure to parse dates. Consider setting index column to 'date'.)
original = pd.read_csv('fcc-forum-pageviews.csv', index_col=0, parse_dates=True)
# Clean data
df = original.copy()
# print("first quantile: ", df.quantile(0.975), "second quantile: ", df.quantile(0.025))
mask = (df["value"] <= df["value"].quantile(0.975)) & (df["value"] >= df["value"].quantile(0.025))
df = df[mask]

# print(df)

def draw_line_plot():
    # Draw line plot
    fig, ax = plt.subplots()
    df.plot(kind="line", ax=ax, color="r")
    plt.xticks(rotation = 0)
    plt.yticks(rotation = 0)
    ax.set_xlabel("Date")
    ax.set_ylabel("Page Views")
    ax.set_title("Daily freeCodeCamp Forum Page Views 5/2016-12/2019")
    plt.legend().remove()
    # plt.show()
    # Save image and return fig (don't change this part)
    fig.savefig('line_plot.png')
    return fig

def draw_bar_plot():
    # Copy and modify data for monthly bar plot
    df_bar = df.copy()

    # print("All data: ")
    allData = df_bar.groupby([df_bar.index.year, df_bar.index.month])['value'].agg(['sum', 'count'])
    allData['average'] = allData['sum'] / allData['count']
    fullData = [0,0,0,0] + allData["average"].tolist()
    sliced = []
    for n in range(4):
        sliced += [fullData[0:12]]
        fullData = fullData[12:]
    
    columns=["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
    # Draw bar plot
    data = {
        "x": sliced,
        "xlabels" : [2016, 2017, 2018, 2019],
    }
    frame = pd.DataFrame(data["x"], index=data["xlabels"])
    fig, ax = plt.subplots()
    frame.plot(kind="bar", ax=ax)
    ax.set_ylabel("Average Page Views")
    ax.set_xlabel("Years")
    ax.legend(columns).set_title("Months")
    # plt.show()


    # Save image and return fig (don't change this part)
    fig.savefig('bar_plot.png')
    return fig

def draw_box_plot():
    # Prepare data for box plots (this part is done!)
    df_box = df.copy()
    df_box.reset_index(inplace=True)
    df_box['year'] = [d.year for d in df_box.date]
    df_box['month'] = [d.strftime('%b') for d in df_box.date]

    # Draw box plots (using Seaborn)
    # print(df_box)
    fig, (first, second) = plt.subplots(1,2)
    # plt.figure(figsize=(20,20))
    plt.subplot(1,2,1)
    sns.boxplot(data=df_box, ax=first, x="year", y="value")
    plt.xlabel("Year")
    plt.ylabel("Page Views")
    plt.title("Year-wise Box Plot (Trend)")
    # plt.show()
    df_box.sort_index()
    plt.subplot(1,2,2)
    df_box["month"] = pd.to_datetime(df_box.month, format='%b').dt.month
    # df_box = df_box.sort_values(by='month',inplace=True)
    df_box = df_box.sort_values(by="month")
    df_box["month"] = [d.strftime('%b') for d in df_box.date]
    # print(df_box)
    sns.boxplot(data=df_box, ax=second, x="month", y="value")
    plt.xlabel("Month")
    plt.ylabel("Page Views")
    plt.title("Month-wise Box Plot (Seasonality)")
    # plt.show()


    # Save image and return fig (don't change this part)
    fig.savefig('box_plot.png')
    return fig
