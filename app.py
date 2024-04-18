import streamlit as st
import pandas as pd
import plotly_express as px
import plotly.graph_objects as go
import matplotlib.pyplot as plt


df = pd.read_csv('vehicles_us.csv')
df['manufacturer'] = df['model'].apply(lambda x: x.split()[0])

st.header('Data viewer')
show_manuf_1k_ads = st.checkbox(
    'Include manufacturers with less than 1000 ads')
if not show_manuf_1k_ads:
    df = df.groupby('manufacturer').filter(lambda x: len(x) > 1000)

st.dataframe(df)
st.header('Vehicle types by manufacturer')
st.write(px.histogram(df, x='manufacturer', color='type'))
st.header('Histogram of `condition` vs `model_year`')

# -------------------------------------------------------
# histograms in plotly:
# fig = go.Figure()
# fig.add_trace(go.Histogram(x=df[df['condition']=='good']['model_year'], name='good'))
# fig.add_trace(go.Histogram(x=df[df['condition']=='excellent']['model_year'], name='excellent'))
# fig.update_layout(barmode='stack')
# st.write(fig)
# works, but too many lines of code
# -------------------------------------------------------

# histograms in plotly_express:
st.write(px.histogram(df, x='model_year', color='condition'))
# a lot more concise!
# -------------------------------------------------------

st.header('Compare price distribution between manufacturers')
manufac_list = sorted(df['manufacturer'].unique())
manufacturer_1 = st.selectbox('Select manufacturer 1',
                              manufac_list, index=manufac_list.index('chevrolet'))

manufacturer_2 = st.selectbox('Select manufacturer 2',
                              manufac_list, index=manufac_list.index('hyundai'))
mask_filter = (df['manufacturer'] == manufacturer_1) | (
    df['manufacturer'] == manufacturer_2)
df_filtered = df[mask_filter]
normalize = st.checkbox('Normalize histogram', value=True)
if normalize:
    histnorm = 'percent'
else:
    histnorm = None
st.write(px.histogram(df_filtered,
                      x='price',
                      nbins=30,
                      color='manufacturer',
                      histnorm=histnorm,
                      barmode='overlay'))

# Analyzing Honda v. Toyota

# Filter data for Honda and Toyota
honda_data = df[df['manufacturer'] == 'honda']
toyota_data = df[df['manufacturer'] == 'toyota']

# Calculate average price for each model year
honda_avg_price = honda_data.groupby(
    'model_year')['price'].mean().reset_index()
toyota_avg_price = toyota_data.groupby(
    'model_year')['price'].mean().reset_index()

# Creating plot comparing average price of Hondas and Toyotas by model year
st.header('Average Price of Honda and Toyota Vehicles Over the Years')
fig = px.line(honda_avg_price, x='model_year', y='price',
              title='Average Price of Honda Vehicles Over the Years')
fig.add_scatter(x=toyota_avg_price['model_year'],
                y=toyota_avg_price['price'], mode='lines', name='Toyota')
fig.update_layout(xaxis_title='Model Year', yaxis_title='Average Price')
st.plotly_chart(fig)

# Calculate number of days listed for each model year
honda_days_listed = honda_data.groupby(
    'model_year')['days_listed'].mean().reset_index()
toyota_days_listed = toyota_data.groupby(
    'model_year')['days_listed'].mean().reset_index()

# Creating plot for number of days listed for sale of Hondas and Toyotas by model year
st.title('Average Number of Days Listed for Honda vs Toyota Vehicles by Model Year')
fig = px.scatter(honda_days_listed, x='model_year', y='days_listed',
                 title='Average Number of Days Listed for Honda Vehicles by Model Year')
fig.add_scatter(x=toyota_days_listed['model_year'],
                y=toyota_days_listed['days_listed'], mode='markers', name='Toyota')
fig.update_layout(xaxis_title='Model Year',
                  yaxis_title='Average Number of Days Listed')
st.plotly_chart(fig)

# Filter out rows with NaN values in the 'odometer' column for Honda and Toyota data
honda_data_filtered = honda_data.dropna(subset=['odometer'])
toyota_data_filtered = toyota_data.dropna(subset=['odometer'])

# Calculate average odometer reading for each model year for Honda and Toyota
honda_avg_odometer = honda_data_filtered.groupby(
    'model_year')['odometer'].mean().reset_index()
toyota_avg_odometer = toyota_data_filtered.groupby(
    'model_year')['odometer'].mean().reset_index()

# Create a DataFrame to hold the combined data
combined_data = pd.merge(honda_avg_odometer, toyota_avg_odometer,
                         on='model_year', suffixes=('_honda', '_toyota'))

# Creating plot comparing odometer by model year of Hondas and Toyotas
st.title('Average Odometer Reading by Model Year for Honda and Toyota')
fig = px.bar(combined_data, x='model_year', y=['odometer_honda', 'odometer_toyota'],
             title='Average Odometer Reading by Model Year for Honda and Toyota',
             labels={'model_year': 'Model Year',
                     'value': 'Average Odometer', 'variable': 'Manufacturer'},
             barmode='group', width=800, height=500)
st.plotly_chart(fig)
