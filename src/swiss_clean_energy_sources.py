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
import json

# st.sidebar.header("Election Exploration")
# 4. Add a suitable title to your app.
st.sidebar.title("Plotting using Streamlit") # this can be added anywhere!
st.header("Clean Energy Sources in Switzerland")

##### Load data

@st.cache
def load_data(path):
    df = pd.read_csv(path)
    return df

df_raw = load_data(path='./data/raw/renewable_power_plants_CH.csv')
df = deepcopy(df_raw)

#geo_df_raw = pd.read_json('./data/raw/georef-switzerland-kanton.geojson')
with open("./data/raw/georef-switzerland-kanton.geojson") as response:
    geo_df_raw = json.load(response)
geo_df = deepcopy(geo_df_raw)



# 1. Create a checkbox Show dataframe to display/hide your dataset.
##### Show Datasets

### Widgets: Checkbox
if st.sidebar.checkbox("Show DataFrame", value=True):
    st.subheader("Dataset")
    st.text('Renewable Power Plants in Switzerland')
    st.dataframe(data=df)
    st.text('Swiss Geographic Kanton Data')
    st.dataframe(data=geo_df)



# 2. Create a Plotly choropleth map, which visualizes the geospatial features and some interesting information from your dataset.
# Add a dropdown that lets users select based on some feature of your dataset (e.g. age of the dog owner).

# Add “All” option to this dropdown.
##### Plotting

st.subheader("Plotting")

## to match Canton code (in df) to Canton name (in geo_df)
cantons_dict = {'TG':'Thurgau', 'GR':'Graubünden', 'LU':'Luzern', 'BE':'Bern', 'VS':'Valais', 
                'BL':'Basel-Landschaft', 'SO':'Solothurn', 'VD':'Vaud', 'SH':'Schaffhausen', 'ZH':'Zürich', 
                'AG':'Aargau', 'UR':'Uri', 'NE':'Neuchâtel', 'TI':'Ticino', 'SG':'St. Gallen', 'GE':'Genève', 
                'GL':'Glarus', 'JU':'Jura', 'ZG':'Zug', 'OW':'Obwalden', 'FR':'Fribourg', 'SZ':'Schwyz', 
                'AR':'Appenzell Ausserrhoden', 'AI':'Appenzell Innerrhoden', 'NW':'Nidwalden', 'BS':'Basel-Stadt'}

## processing data 
df['canton_name'] = df['canton'].map(cantons_dict)
sources_per_canton = df.groupby(by=['canton_name']).agg({
    'production': 'sum',
    'project_name': 'count',
    'electrical_capacity': 'sum'
}).rename(columns={
    'production': 'production',
    'project_name': 'projects',
    'canton_name': 'canton_name'
}).reset_index()

#st.dataframe(data=sources_per_canton)

## Show chosen Canton only

# Widget: Selectbox
canton_names = ["All"] + sorted(pd.unique(sources_per_canton['canton_name']))
chosen_canton_name = st.sidebar.selectbox('Choose a Canton', options=canton_names)

# Widget: Ratio
project_num = st.sidebar.radio(
    "Show canton with projects",
    ('All', 'less than 1000', 'from 1000 to less than 2000', 'more than 2000'))

if 'All' == chosen_canton_name:
    if project_num == 'All':
        reduced_df = sources_per_canton
    elif project_num == 'less than 1000':
        reduced_df = sources_per_canton[sources_per_canton['projects'] < 1000]
    elif project_num == 'from 1000 to less than 2000':
        reduced_df = sources_per_canton[(sources_per_canton['projects'] >= 1000) & (sources_per_canton['projects'] < 2000)]
    else:
        reduced_df = sources_per_canton[sources_per_canton['projects'] >= 2000]
else:
    if project_num == 'All':
        reduced_df = sources_per_canton[sources_per_canton['canton_name'] == chosen_canton_name]
    elif project_num == 'less than 1000':
        reduced_df = sources_per_canton[(sources_per_canton['canton_name'] == chosen_canton_name) & (sources_per_canton['projects'] < 1000)]
    elif project_num == 'from 1000 to less than 2000':
        reduced_df = sources_per_canton[(sources_per_canton['canton_name'] == chosen_canton_name) & (sources_per_canton['projects'] >= 1000) & (reduced_df['projects'] < 2000)]
    else:
        reduced_df = sources_per_canton[(sources_per_canton['canton_name'] == chosen_canton_name) & (sources_per_canton['projects'] >= 2000)]

fig = px.choropleth_mapbox( #we also can use px.choropleth() for a world map (geoJSON file not required!)
    reduced_df, 
    geojson=geo_df_raw, 
    color="projects",
    locations="canton_name", 
    featureidkey="properties.kan_name",
    center={"lat": 46.8, "lon": 8.3},
    mapbox_style="carto-positron",
    opacity=0.8,
    width=800,
    height=600,
    hover_data=['electrical_capacity', 'production'],
    zoom=6,
    title='Clean Energy Sources in Switzerland', # <<< this doesn't make any changes!
)
fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
st.plotly_chart(fig)





# 3. Create a bar chart or a scatter plot for your dataset.
# Add a radio button that lets users choose to display two different options (e.g. male/female or before/after).
# Optional: Can you make this button work on both of your plots simultaneously?

fig2 = px.scatter(
        reduced_df, 
        x='canton_name', y='projects', opacity=0.5,
        # range_x=[1, 8], range_y=[10, 50],
        width=1000, height=800,
        labels={'canton_name': 'Cantons (Cities)', 'projects': 'Project number'},
        title='Number of energy projects per Canton',
        hover_data=['electrical_capacity', 'production', 'projects'], ### how to add html elements & styling?
    )
fig2.update_layout(title_font_size=22)
fig2.update_layout(showlegend=False)
fig2.update_traces(
    marker=dict(size=12, line=dict(width=2,color='red')),
    selector=dict(mode='markers'))
st.plotly_chart(fig2)


# 5. Further customize your app as you like (e.g. add a sidebar, split the page into columns, add text, etc.).




# 6. Once you’re satisfied with your app, move on to the deployment page.