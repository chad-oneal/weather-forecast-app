# import streamlit for GUI, plotly for the graph
# import backend to utilize the api from https://openweathermap.org/
import streamlit as st
import plotly as px
import pytz
from datetime import datetime
from backend import get_data

# Structure of GUI
st.title('Weather Forecast')
location = st.text_input('Location: ')
days = st.slider('Forecast Days', min_value=1, max_value=5,
                 help='Select the number of forecasted days')
option = st.selectbox("Select data to View",
                      ("Temperature", "Cloud Cover"))
st.subheader(f'{option} for the next {days} days in {location}')

# Get Temperature and Cloud Cover conditions
if location:
    try:
        filtered_data = get_data(location, days)

        # Define the EST timezone
        est = pytz.timezone('US/Eastern')

        # Conditional to return temperature & date data from API data list and dictionaries
        if option == 'Temperature':
            temperatures = [round((dict['main']['temp'] - 273.15) * 9 / 5 + 32, 1) for dict in filtered_data]

            # Convert UTC to EST and format for 12-hour clock with AM/PM
            dates = [datetime.strptime(dict['dt_txt'], '%Y-%m-%d %H:%M:%S')
                     .replace(tzinfo=pytz.utc).astimezone(est).strftime('%Y-%m-%d %I:%M %p')
                     for dict in filtered_data]
            # Create a temperature plot
            figure = px.line(x=dates, y=temperatures, labels={'x': 'Date', 'y': 'Temperature (F)'})
            # Rotate the x-axis labels and limit the number of ticks
            figure.update_layout(xaxis=dict(tickangle=0, nticks=5))
            st.plotly_chart(figure)

        # Conditional to return cloud cover from API data list and dictionaries
        if option == 'Cloud Cover':
            images = {'Clear': 'images/clear.png', 'Clouds': 'images/cloud.png',
                      'Snow': 'images/snow.png', 'Rain': 'images/rain.png'}

            cloud_cover = [dict['weather'][0]['main'] for dict in filtered_data]
            image_paths = [images[condition] for condition in cloud_cover]

            # Extracting dates for each forecast
            dates = [datetime.strptime(dict['dt_txt'], '%Y-%m-%d %H:%M:%S')
                     .replace(tzinfo=pytz.utc).astimezone(est).strftime('%Y-%m-%d %I:%M %p')
                     for dict in filtered_data]

            # Define the number of images per row
            images_per_row = 5

            # Iterate over each cloud condition and its corresponding date
            for index, (image_path, date) in enumerate(zip(image_paths, dates)):
                # For every 'images_per_row' images, start a new row
                if index % images_per_row == 0:
                    cols = st.columns(images_per_row)

                # Display the image in the appropriate column
                with cols[index % images_per_row]:
                    st.image(image_path, width=115)
                    st.caption(date)

    except KeyError:
        st.write('This location does not exist')