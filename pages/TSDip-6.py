import pandas as pd
import numpy as np
from datetime import datetime
import os

import plotly.graph_objects as go
from plotly.subplots import make_subplots
#import plotly.io as pio


import streamlit as st

##### HANDLING THE DATA

target = 'TSDip-6.txt'

df = pd.read_csv(f"/home/rod/Documents/DataScience/my_projects/tsdip/data/{target}",sep="\t")    # reading the file

### Cleaning up and refactoring column names

# droping unused columns
df.drop(['SS','FileName','Ser','Meas ','Sal. ','Cond. ','Temp ',' %O2 ','mg/l'],axis=1,inplace=True) 
# renaming columns
df.columns=['SoS','Depth','year','month','day','hour','minute','second']                             
# keep only  depths above 2.0 meters
df = df[df['Depth']>2.0]            
# parsing datetime columnes to single 'date' columns
df['date']=pd.to_datetime(df[['year', 'month', 'day', 'hour','minute','second']])     

# dealing with time to calculate deployment and recovery speed
df['time_shift'] = df['date'].shift()
df['time_diff']=(df['date']-df['time_shift'])/ pd.Timedelta(seconds=1)
df['depth_shifted']=df['Depth'].shift()
df['depth_step(m)']=abs(df['Depth']-df['depth_shifted'])
df['dip_speed(m/s)'] = abs(df['depth_step(m)']/df['time_diff'])
# cleaning up temp columns
df.drop(['time_shift','time_diff','depth_shifted','depth_step(m)','year', 'month', 'day', 'hour','minute','second'],axis=1,inplace=True)

# finalizing the dataframe
# spliting date and time in sperate columns
df["Date"] = df["date"].dt.date                                                                      
df["Time"] = df["date"].dt.time                                                                      
# droping unused columns and reseting indexes
df.drop("date",axis=1,inplace=True)                                                                  
df.reset_index(inplace=True)                                                                         
df.reset_index(inplace=True)                                                                         


### defining dip direction (up or down)
# find index of the max depth value
tmax=df['Time'][df['Depth']==df['Depth'].max()].index        
# create 'direction' columns based on index level
df['direction'] = np.where(df['level_0']<=tmax[0], 'down', 'up')                                    
# remove unused column
df.drop(['level_0','index'],axis=1,inplace=True)                                                    

### spliting dataframe by direction and depth
# full column dataframe for each direction
df_up=df[df['direction']=='up']
df_down=df[df['direction']=='down']

### exporting the downwards profile to be compiled in the home page - all profiles
df_down[['SoS','Depth']].to_csv(f"/home/rod/Documents/DataScience/my_projects/tsdip/home_files/{target[0:7]}.csv")

# top 50m dataframe in each direction
top = df[df['Depth']<=50] 
top_up=top[top['direction']=='up']
top_down=top[top['direction']=='down']






##### BUILDING THE GRAPHS

## SPEED OF SOUND PROFILES

## FULL COLUMN
fig = make_subplots(
    rows=1,cols=1)

fig.add_trace(
    go.Scatter(x=df_down['SoS'],y=df_down['Depth'],line=dict(color='royalblue'),name="down"),
    row=1,col=1
)

fig.add_trace(
    go.Scatter(x=df_up['SoS'],y=df_up['Depth'],line=dict(color='brown'),name="up",),
    row=1,col=1
)

fig.update_yaxes(autorange="reversed", row=1, col=1)

fig.update_layout(
    xaxis={'side':'top'},
    xaxis_title="Speed of sound (m/s)",
    yaxis_title="Depth (m)",
    legend_title="direction",
    template='ggplot2',
    height=800,
    width=600,
    
    
)

## TOP 50m
fig2 = make_subplots(
    rows=1,cols=1)

fig2.add_trace(
    go.Scatter(x=top_down["SoS"],y=top_down["Depth"],line=dict(color='royalblue'),name='down'),
    row=1,col=1
)

fig2.add_trace(
    go.Scatter(x=top_up["SoS"],y=top_up["Depth"],line=dict(color='brown'),name='up'),
    row=1,col=1
)


fig2.update_yaxes(autorange="reversed", row=1, col=1)

fig2.update_layout(
    xaxis={'side':'top'},
    xaxis_title="Speed of sound (m/s)",
    yaxis_title="Depth (m)",
    legend_title="direction",
    template='ggplot2',
    height=800,
    width=600,
)


############
# DEPLOYMENT SPEED

fig3 = make_subplots(
    rows=1,cols=1)

fig3.add_trace(
    go.Scatter(x=df_down['dip_speed(m/s)'],y=df_down['Depth'],line=dict(color='royalblue'),showlegend=False),
    row=1,col=1
)

fig3.update_yaxes(autorange="reversed", row=1, col=1)

fig3.update_layout(
    xaxis={'side':'top'},
    xaxis_title="Speed (m/s)",
    yaxis_title="Depth (m)",
    template='ggplot2',
    height=800,
    width=600,
    
    
)

# RECOVERY SPEED
fig4 = make_subplots(
    rows=1,cols=1)

fig4.add_trace(
    go.Scatter(x=df_up['dip_speed(m/s)'],y=df_up['Depth'],line=dict(color='brown'),showlegend=False),
    row=1,col=1
)

fig4.update_yaxes(autorange="reversed", row=1, col=1)

fig4.update_layout( 
    xaxis={'side':'top'},
    xaxis_title="Speed (m/s)",
    yaxis_title="Depth (m)",
    template='ggplot2',
    height=800,
    width=600,
    
    
)

#### DASHBOARD LAYOUT
# "Speed of sound profile (m/s)"

col1, col2 = st.columns(2,gap="medium")

with col1:
    st.text("Full column profile")
    st.plotly_chart(fig)

with col2:
    st.text("Top 50m")
    st.plotly_chart(fig2)

# "Deployment/recovery speed (m/s)"

col1, col2 = st.columns(2,gap="medium")

with col1:
    st.text("Deṕloyment speed (m/s)")
    st.plotly_chart(fig3)

with col2:
    st.text("Recovery speed (m/s)")
    st.plotly_chart(fig4)