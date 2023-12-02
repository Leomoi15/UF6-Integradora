import streamlit as st
import pandas as pd
import numpy as np
import plotly as px
import plotly.figure_factory as ff
from bokeh.plotting import figure
import matplotlib.pyplot as plt

st.set_page_config(page_title="PIR", page_icon=":bar_chart:", layout="wide")

st.title("San Francisco Police Incident Reports (2018-2020)")
st.subheader("Exploring Crime Data Across Police Districts")

df = pd.read_csv("Police_Department_Incident_Reports__2018_to_Present.csv")
st.markdown("The data shown below  belongs to incident reports in the city of San francisco, from the year 2018 to 2020, with details from each case such as date, day of the week, police districts, neighborhood in which it happened, type of incidentin category and subcategory, exact location and resoluntion.")

##Cambio
st.markdown(f"Total Incidents: {len(df)}")
st.markdown(f"Start Date: {df['Incident Date'].min()}")
st.markdown(f"End Date: {df['Incident Date'].max()}")

mapa = pd.DataFrame()
mapa['Date'] = df['Incident Date']
mapa['Day'] = df['Incident Day of Week']
mapa['Police District'] = df['Police District']
mapa['Neighborhood'] = df['Analysis Neighborhood']
mapa['Incident Category'] = df['Incident Category']
mapa['Incident Subcategory'] = df['Incident Subcategory']
mapa['Resolution'] = df['Resolution']
mapa['lat'] = df['Latitude']
mapa['lon'] = df['Longitude']
mapa = mapa.dropna()

subset_data2 = mapa
police_district_input = st.sidebar.multiselect(
'Police District',
mapa.groupby('Police District').count().reset_index()['Police District'].tolist())
if len(police_district_input) > 0:
    subset_data2 = mapa[mapa['Police District'].isin(police_district_input)]

subset_data1 = subset_data2
neighborhood_input = st.sidebar.multiselect(
'Neighborhood',
subset_data2.groupby('Neighborhood').count().reset_index()['Neighborhood'].tolist())
if len(neighborhood_input) > 0:
    subset_data1 = subset_data2[subset_data2['Neighborhood'].isin(neighborhood_input)]

subset_data = subset_data1
incident_input = st.sidebar.multiselect(
    'Incident Category',
    subset_data1.groupby('Incident Category').count().reset_index()['Incident Category'].tolist())

if len(incident_input) > 0:
    subset_data = subset_data1[subset_data1['Incident Category'].isin(incident_input)]

subset_data

st.markdown('It is important to mention that any police district can aswer to any incident, the neighborhood in which it happened is not related to the police distrcit')
st.markdown('Crime locations in San Francisco')
st.map(subset_data)
st.markdown('Crimes ocurred per day of teh week')
st.bar_chart(subset_data['Day'].value_counts())
st.markdown('Crime ocurred per date')
st.line_chart(subset_data['Date'].value_counts())
st.markdown('Type of crimmes commited')
st.bar_chart(subset_data['Incident Category'].value_counts())

agree = st.button('Click to see Incident Subcategories')
if agree:
    st.markdown('Subtype of crimes committed')
    st.bar_chart(subset_data['Incident Subcategory'].value_counts())


st.markdown('Resolution status')
fig1, ax1 = plt.subplots()
labels = subset_data['Resolution'].unique()
ax1.pie(subset_data['Resolution'].value_counts(), labels = labels, autopct='%1.1f%%', startangle = 20)
st.pyplot(fig1)

##Cambio
import plotly.express as px

neighborhood_counts = subset_data['Neighborhood'].value_counts()

fig_neighborhood = px.bar(x=neighborhood_counts.index, y=neighborhood_counts.values,
                          labels={'x': 'Neighborhood', 'y': 'Number of Incidents'},
                          title='Incidents Distribution by Neighborhood',
                          color=neighborhood_counts.index,
                          color_discrete_sequence=px.colors.qualitative.Set3)

st.plotly_chart(fig_neighborhood)

#Cambio
district_counts = subset_data['Police District'].value_counts()

fig_district = px.bar(x=district_counts.index, y=district_counts.values,
                      labels={'x': 'Police District', 'y': 'Number of Incidents'},
                      title='Incidents Distribution by Police District',
                      color=district_counts.index,
                      color_discrete_sequence=px.colors.qualitative.Set3)

st.plotly_chart(fig_district)

##Cambio
import plotly.express as px

heatmap_data = subset_data.groupby(['lat', 'lon']).size().reset_index(name='incident_count')
fig_heatmap = px.density_mapbox(heatmap_data, lat='lat', lon='lon', z='incident_count',
                                radius=15, center=dict(lat=37.77, lon=-122.42),
                                zoom=10, mapbox_style="carto-positron",
                                labels={'incident_count': 'Incident Count'},
                                title='Incident Density Map')

fig_heatmap.update_layout(margin=dict(t=0, l=0, r=0, b=0))
st.plotly_chart(fig_heatmap)

##Cambio
st.markdown("Source: [San Francisco Police Department](https://data.sfgov.org/Public-Safety/Police-Department-Incident-Reports-2018-to-Present/wg3w-h783)")
