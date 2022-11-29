# Standard imports
import pandas as pd

# matplotlib
import matplotlib as mpl
import matplotlib.pyplot as plt
import seaborn as sns

#plotly
import plotly.express as px
import plotly.graph_objects as go

#streamlit
import streamlit as st

#others
from copy import deepcopy

# Add title & header
st.sidebar.title("Maps & Advanced customization")
st.sidebar.header("Election Exploration")
st.header("Election Exploration")

geojson = px.data.election_geojson()
ds = px.data.election()
df = deepcopy(ds)

### Widgets: Checkbox (you can replace st.xx with st.sidebar.xx)
if st.sidebar.checkbox("Show DataFrame", key=1, value=False): # <<< key is used for multi checkboxes with the same label!
    st.subheader("Election Dataset")
    st.dataframe(data=df)
    st.subheader("District Geography Data")
    st.dataframe(data=deepcopy(geojson))

fig = px.choropleth_mapbox(
    ds, 
    geojson=geojson, 
    color="winner",
    locations="district", 
    featureidkey="properties.district",
    center={"lat": 45.5517, "lon": -73.7073},
    mapbox_style="carto-positron", 
    zoom=9
)
fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
st.plotly_chart(fig)




### UNEMPLOYMENT RATE EXPLORATION
st.sidebar.header("Unemployment Rate Exploration")
st.header("Unemployment Rate Exploration")

from urllib.request import urlopen
import json 
with urlopen('https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json') as response:
    counties = json.load(response)
df2 = pd.read_csv("https://raw.githubusercontent.com/plotly/datasets/master/fips-unemp-16.csv", dtype={"fips": str})

if st.sidebar.checkbox("Show DataFrame", key=2, value=False):
    st.subheader("Unemployment Rate Dataset")
    st.dataframe(data=df2)
    st.subheader("County Geography Data")
    st.dataframe(data=deepcopy(counties))

fig2 = go.Figure(
    go.Choroplethmapbox(
        geojson=counties, locations=df2.fips, z=df2.unemp,
        colorscale="Viridis", zmin=0, zmax=12,
        marker_opacity=0.5, marker_line_width=0
    )
)
fig2.update_layout(
    mapbox_style="carto-positron",
    mapbox_zoom=3, 
    mapbox_center = {"lat": 37.0902, "lon": -95.7129}
)
fig2.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
st.plotly_chart(fig2)