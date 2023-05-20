# python -m streamlit run people_in_space.py

import requests
import streamlit as st

def get_people_in_space():
    response = requests.get("http://api.open-notify.org/astros.json")
    if response.status_code == 200:
        data = response.json()
        return data['number'], [person['name'] for person in data['people']]
    else:
        return None, []

def get_iss_location():
    response = requests.get("http://api.open-notify.org/iss-now.json")
    if response.status_code == 200:
        data = response.json()
        location = data['iss_position']
        latitude = float(location['latitude'])
        longitude = float(location['longitude'])
        return latitude, longitude
    else:
        return None, None

import pandas as pd  # import pandas at the top of your file

def main():
    st.title("People in Space and ISS Location")
    st.markdown("This application displays the total number of people in space, their names, and the current location of the International Space Station (ISS).")

    number_of_people, people_names = get_people_in_space()
    if number_of_people is not None:
        st.write("Total number of people in space:", number_of_people)
        st.write("Names of people in space:")
        for name in people_names:
            st.write("- " + name)
    else:
        st.write("Failed to retrieve people data")

    latitude, longitude = get_iss_location()
    if latitude is not None and longitude is not None:
        st.write("Current ISS Location:")
        # Create a pandas dataframe with proper column names
        df = pd.DataFrame({
            'lat': [latitude],
            'lon': [longitude]
        })
        st.map(df, zoom=1)
        st.write("Latitude:", latitude)
        st.write("Longitude:", longitude)
    else:
        st.write("Failed to retrieve ISS location")


if __name__ == '__main__':
    main()
