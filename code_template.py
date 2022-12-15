import pandas as pd
import numpy as np
from datetime import datetime
import os

import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import plotly.io as pio
import plotly.express as px

import streamlit as st

##### HANDLING THE DATA

target = 'target-name'

df = pd.read_csv(f"/home/rod/Documents/DataScience/my_projects/nav/tsdip/data/{target}",sep="\t")    # reading the file
df.drop(['SS','FileName','Ser','Meas ','Sal. ','Cond. ','Temp ',' %O2 ','mg/l'],axis=1,inplace=True) # droping unused columns
df.columns=['SoS','Depth','year','month','day','hour','minute','second']                             # renaming columns
df = df[df['Depth']>2.0]                                                                             # keep only  depths above 2.0 meters
df['date']=pd.to_datetime(df[['year', 'month', 'day', 'hour','minute','second']])                    # parsing datetime columnes to single 'date' columns
df.drop(['year', 'month', 'day', 'hour','minute','second'],axis=1,inplace=True)                      # droping date and time not to be used
df["Date"] = df["date"].dt.date                                                                      # splitting date
df["Time"] = df["date"].dt.time                                                                      # spliting time
df.drop("date",axis=1,inplace=True)                                                                  # droping single 'datetime' column
df.reset_index(inplace=True)                                                                         # reset index
df.reset_index(inplace=True)                                                                         # reset index again to get correct index column
tmax=df['Time'][df['Depth']==df['Depth'].max()].index                                                # find index of the max depth value
df['direction'] = np.where(df['level_0']<=tmax[0], 'down', 'up')                                     # create 'direction' columns based on index level
df.drop(['level_0','index'],axis=1,inplace=True)                                                     # remove unused column
df_up=df[df['direction']=='up']                                                                      # recovering  the probe
df_down=df[df['direction']=='down']                                                                  # deploying the probe
top = df[df['Depth']<=50]                                                                            # top 50m water column
top_up=top[top['direction']=='up']                                                                   # top 50 during recovery
top_down=top[top['direction']=='down']                                                               # top 50 during deployment            

##### BUILDING THE GRAPHS

## SUB-PLOTS WITH FULL COLUMN AND TOP 50m SPEED OF SOUND DATA  
fig = make_subplots(
    rows=1,cols=2,
    subplot_titles=("Full column","Top 50m")
)

fig.add_trace(
    go.Scatter(x=df_down['SoS'],y=df_down['Depth'],line=dict(color='royalblue'),showlegend=False),
    row=1,col=1
)

fig.add_trace(
    go.Scatter(x=df_up['SoS'],y=df_up['Depth'],line=dict(color='orange'),showlegend=False),
    row=1,col=1
)

fig.add_trace(
    go.Scatter(x=top_down["SoS"],y=top_down["Depth"],mode='lines+markers',line=dict(color='royalblue'),name='down'),
    row=1,col=2
)

fig.add_trace(
    go.Scatter(x=top_up["SoS"],y=top_up["Depth"],mode='lines+markers',line=dict(color='orange'),name='up'),
    row=1,col=2
)

fig.update_yaxes(autorange="reversed", row=1, col=1)
fig.update_yaxes(autorange="reversed", row=1, col=2)
fig.update_xaxes(range=[1539,1543],row=1,col=2)

fig.update_layout(
    #title_text="Speed of sound profile (m/s)",
    xaxis2={'side':'top'},
    xaxis={'side':'top'},
    yaxis_title="Depth (m)",
    yaxis2_title="Depth (m)",
    legend_title="direction",
    template='seaborn',
    height=1000,
    width=1200,
    
)
fig.update_annotations(yshift=20)

############
# DEPLOYMENT SPEED




#### DASHBOARD LAYOUT
st.subheader("Speed of sound profile (m/s)")

st.plotly_chart(fig)

st.subheader("Deployment speed")