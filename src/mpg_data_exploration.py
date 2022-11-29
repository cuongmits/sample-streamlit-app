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
st.sidebar.title("Introduction to Streamlit")
st.header("MPG Data Exploration")

@st.cache
def load_data(path):
    df = pd.read_csv(path)
    return df

mpg_df_raw = load_data(path='./data/raw/mpg.csv')
mpg_df = deepcopy(mpg_df_raw)

### Widgets: Checkbox (you can replace st.xx with st.sidebar.xx)
if st.sidebar.checkbox("Show DataFrame", value=True):
    st.subheader("Dataset")
    #st.table(data=mpg_df) #this will display all table without scrollbar
    st.dataframe(data=mpg_df)
    
### Widgets: Ratio
plot_type = st.sidebar.radio(
    "Choose Plot type",
    ('Plotly', 'Matplotlib'))

### Widgets: Selectbox
st.subheader("Highway Fuel Efficiency")

## process Year
years = ["All"] + sorted(pd.unique(mpg_df['year']))
year = st.sidebar.selectbox('Choose a Year', options=years)
if 'All' == year:
    reduced_df = mpg_df
else:
    reduced_df = mpg_df[mpg_df['year'] == year]

## process Class
classes = ["All"] + sorted(pd.unique(mpg_df['class']))
chosen_class = st.sidebar.selectbox('Choose a Class', options=classes)
if 'All' == chosen_class:
    if 'All' == year:
        reduced_df = mpg_df
    else:
        reduced_df = mpg_df[mpg_df['year'] == year]
else:
    if 'All' == year:
        reduced_df = mpg_df[mpg_df['class'] == chosen_class]
    else:
        reduced_df = mpg_df[(mpg_df['year'] == year) & (mpg_df['class'] == chosen_class)]

### Widgets: Ratio
show_mean = st.sidebar.radio(
    "Show Class Means",
    ('Yes', 'No'))

## means
if show_mean == 'Yes':
    means = reduced_df.groupby('class').mean()
show_means_text = 'to show means' if show_mean == 'Yes' else 'not to show means'
    
st.markdown(
    f'You selected: \
        <span style="color:red">**{year}**</span> year, \
        <span style="color:red">**{chosen_class}**</span> class, \
        and <span style="color:red">**{show_means_text}**</span>.',
    unsafe_allow_html=True)

if plot_type == 'Matplotlib': # then display in Matplotlib
    m_fig, ax = plt.subplots(figsize=(10,8))
    ax.scatter(reduced_df['displ'], reduced_df['hwy'], alpha=0.7)

    ax.set_title("Engine Size vs Highway Fuel Mileage")
    ax.set_xlabel('Displacement (Liters)')
    ax.set_ylabel('MPG')

    if show_mean == 'Yes':
        ax.scatter(means['displ'], means['hwy'], alpha=0.7, color='red')

    st.pyplot(m_fig)
else: # then display in Plotly
    p_fig = px.scatter(
        reduced_df, x='displ', y='hwy', opacity=0.5,
        range_x=[1, 8], range_y=[10, 50],
        width=800, height=600,
        labels={'displ': 'Displacement (Liters)', 'hwy': 'MPG'},
        title='Engine Size vs Highway Fuel Mileage',
        hover_data=['manufacturer', 'model'], ### how to add html elements & styling?
        #text=reduced_df['manufacturer'] #
    )
    p_fig.update_layout(title_font_size=22)
    
    if show_mean == 'Yes':
        p_fig.add_trace(go.Scatter(x=means['displ'], y=means['hwy'], mode='markers'))
    
    p_fig.update_layout(showlegend=False)
    st.plotly_chart(p_fig)
