import streamlit as st
import folium
from folium.plugins import MarkerCluster
from dotenv import load_dotenv
import os
import google.generativeai as genai
import requests
from bs4 import BeautifulSoup
#from itinerary_display import display_itinerary_tiles

#from streamlit_folium import folium_static


def display_folium_map(locations):
    # Initialize the mapgit
    m = folium.Map(location=[41.8781, -87.6298], zoom_start=12)  # Default location is Chicago

    # Add markers to the map
    for location in locations:
        folium.Marker(location).add_to(m)

    # Convert the map to HTML
    html_code = m._repr_html_()

    return html_code
# # Custom CSS to hide the Streamlit branding and adjust the layout
# hide_streamlit_style = """
# <style>
#     #MainMenu {visibility: hidden;}
#     footer {visibility: hidden;}
#     .stTextInput > div > div > input {
#         padding-right: 4em !important;
#     }
#     .stButton > button {
#         margin-top: -36px;
#         margin-left: auto;
#         height: 2.1em;
#         border-radius: 0 4px 4px 0;
#     }
#     .stTextInput > div > div {
#         position: relative;
#     }
# </style>
# """

# # Function to display HTML/JavaScript for geolocation
# def get_location():
#     geolocation_html = """
#     <script>
#     function getLocation() {
#         if (navigator.geolocation) {
#             navigator.geolocation.getCurrentPosition(showPosition, showError);
#         } else {
#             alert('Geolocation is not supported by this browser.');
#         }
#     }
#     function showPosition(position) {
#         const lat = position.coords.latitude;
#         const lon = position.coords.longitude;
#         const message = {lat: lat, lon: lon};
#         window.parent.postMessage({type: 'streamlit:setComponentValue', data: message}, '*');
#     }
#     function showError(error) {
#         switch(error.code) {
#             case error.PERMISSION_DENIED:
#                 alert('User denied the request for Geolocation.');
#                 break;
#             case error.POSITION_UNAVAILABLE:
#                 alert('Location information is unavailable.');
#                 break;
#             case error.TIMEOUT:
#                 alert('The request to get user location timed out.');
#                 break;
#             case error.UNKNOWN_ERROR:
#                 alert('An unknown error occurred.');
#                 break;
#         }
#     }
#     </script>
#     """
#     # components.html(geolocation_html, height=0, width=0)
#     st.write(geolocation_html, unsafe_allow_html=True)

# # Initialize the backend setup
# def setup_backend():
#     load_dotenv()
#     api_key = os.getenv('API_KEY')
#     # google_maps_api_key = os.getenv('GOOGLE_MAPS_API_KEY')
#     genai.configure(api_key=api_key)

#     generation_config = {
#         "temperature": 0.9,
#         "top_p": 1,
#         "top_k": 1,
#         "max_output_tokens": 2048,
#     }

#     safety_settings = [
#         {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
#         {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
#         {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
#         {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
#     ]

#     model = genai.GenerativeModel(model_name="gemini-1.0-pro", generation_config=generation_config,
#                                   safety_settings=safety_settings)
#     return model

# model = setup_backend()
# itinerary_json = {}

# # Function to get the itinerary based on user input
# def get_itinerary(user_location, days, must_go_places, food_preferences, budget):
#     prompt = f'''You are a Travel advisor GPT, your task is to give a list of itineraries, based on user inputs like :
# City :
# User Location :
# No of days they are staying :
# Food Interests:(List of Cuisines)
# Locations user wants to for sure visit :
# Budget of the user: (Budget Friendly, No Cost Preference)
# if user says “Budget Friendly ” The itineraries should be focused with in 
# 	-  First preference, save budget 
# 	- Second preference to Places user want to visit, Popular locations in that city
# 	- Cover most places they can
# if user says “No Cost Preference ” The itineraries should be focused
# 	- first preference to Places user want to visit, Popular locations in that city
# 	- Cover most places they can

# all itineraies should start from places near user location 
# the list of itineraies should go from low budget to high budget 
# and every itinerary should cover user’s must visit places list as 

# Output should be a json formatted with a list of 4 itineraries
# with each itinerary with unique id having details for for each with List of places with 3 food places with food interests near each place, location and location coordinates for each place , timing of each place and cost of the visit to each place, and google maps location link of that place and day to day places should be optimised by travel time 
# each location should give this text “https://www.google.com/maps/search/?api=1&query=”+latitude+&+longitude 


# Inputs :
# City : Chicago
# User Location : {user_location}
# No of days they are staying : {days}
# Locations user wants to for sure visit :  [{must_go_places}]
# Food Interests: [{food_preferences}] 
# Budget: {budget}'''
#     convo = model.start_chat(history=[])
#     convo.send_message(prompt)
#     try:
#         itinerary_text = convo.last.text
#         # Check if response contains valid data
#         if itinerary_text:
#             # Parse JSON data
#             itinerary_json = json.loads(itinerary_text)
#             return itinerary_json
#         else:
#             st.error("Empty response received from the API.")
#             return {}
#     except Exception as e:
#         st.error(f"Error getting or parsing itinerary: {e}")
#         return {}
# # Collect user input
# user_location = st.text_input('Enter your location')

# # Number of days for tourism
# days = st.number_input('Number of days for tourism', min_value=1, max_value=30)

# # Locations user wants to for sure visit
# must_go_places = st.text_input('Must-go places')

# # Food Preferences
# food_preferences = st.selectbox(
#     'Food Preferences',
#     ['Select a Cuisine', 'Indian', 'Mexican', 'Chinese', 'Italian', 'Thai', 'Japanese', 'French', 'Mediterranean', 'Korean']
# )

# # Budget for the trip
# budget = st.radio(
#     "Budget for the trip",
#     ('Budget Friendly', 'No Cost Preference'),
#     key='budget'
# )

# # Function to save itinerary JSON to a file
# def save_itinerary_to_file(itinerary_json):
#     try:
#         with open("itinerary.json", "w") as outfile:
#             json.dump(itinerary_json, outfile)
#         st.success("Itinerary saved successfully.")
#     except Exception as e:
#         st.error(f"Error saving itinerary to file: {e}")

# # Function to load itinerary JSON from file
# def load_itinerary_from_file():
#     try:
#         with open("itinerary.json", "r") as infile:
#             return json.load(infile)
#     except FileNotFoundError:
#         st.error("Itinerary file not found.")
#         return {}
#     except json.JSONDecodeError as e:
#         st.error(f"Error parsing itinerary JSON: {e}")
#         return {}
    


# # Streamlit app title
# st.title('Tourism Itinerary Viewer')

# # Load itinerary JSON from file
# itinerary_json = load_itinerary_from_file()

# # Number of days for tourism
# num_days = st.number_input('Number of days for tourism', key='num_days', min_value=1, max_value=30)

# #Function to display places in tiles
# def display_places_in_tiles(itinerary_json, num_days):
#     st.header("Itinerary for {} days".format(num_days))
    
#     if "itineraries" in itinerary_json:
#         itineraries = itinerary_json["itineraries"]
        
#         for i, itinerary in enumerate(itineraries, start=1):
#             st.subheader("Itinerary {}".format(i))
#             st.write("Budget: {}".format(itinerary["budget"]))
            
#             for day_num in range(1, num_days + 1):
#                 day_key = "day{}".format(day_num)
#                 if day_key in itinerary:
#                     st.subheader("Day {}".format(day_num))
#                     places = itinerary[day_key]
#                     for place in places:
#                         st.write("Place Name: {}".format(place["place"]))
#                         st.write("Location: {}".format(place["location"]))
#                         st.write("Timing: {}".format(place["timing"]))
#                         st.write("Cost: {}".format(place["cost"]))
#                         st.write("Food Options:")
#                         for food_option in place["food_places"]:
#                             st.write("- Name: {}, Cuisine: {}, Cost: {}".format(
#                                 food_option["name"], food_option["cuisine"], food_option["cost"]))
#                         st.write("---")
#                 else:
#                     st.write("No plan for Day {}".format(day_num))
#             st.write("---")
#     else:
#         st.error("No itinerary data found.")


# # Display places in tiles
# display_places_in_tiles(itinerary_json, num_days)

# # Function to display itinerary based on the days
# def display_itinerary(days):
#     itinerary = load_itinerary_from_file()
#     for i in range(1, days + 1):
#         st.subheader(f"Day {i}")
#         day_key = f"day{i}"
#         if day_key in itinerary:
#             display_places_in_tiles(itinerary[day_key])

# #save it to the file
# if st.button('Generate Itinerary'):
#     itinerary_text = get_itinerary(user_location, days, must_go_places, food_preferences, budget)
#     if itinerary_text:
#         try:
#             itinerary_json = json.loads(itinerary_text)
#             save_itinerary_to_file(itinerary_json)
#             display_itinerary(num_days)
#         except json.JSONDecodeError as e:
#             st.error(f"Error parsing itinerary JSON: {e}")
#     else:
#         st.error("Failed to retrieve itinerary")


import streamlit as st
import streamlit.components.v1 as components
from dotenv import load_dotenv
import os
import google.generativeai as genai

# Custom CSS to hide the Streamlit branding and adjust the layout
hide_streamlit_style = """
<style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    .stTextInput > div > div > input {
        padding-right: 4em !important;
    }
    .stButton > button {
        margin-top: -36px;
        margin-left: auto;
        height: 2.1em;
        border-radius: 0 4px 4px 0;
    }
    .stTextInput > div > div {
        position: relative;
    }
</style>
"""

# Function to display HTML/JavaScript for geolocation
def get_location():
    geolocation_html = """
    <script>
    function getLocation() {
        if (navigator.geolocation) {
            navigator.geolocation.getCurrentPosition(showPosition, showError);
        } else {
            alert('Geolocation is not supported by this browser.');
        }
    }
    function showPosition(position) {
        const lat = position.coords.latitude;
        const lon = position.coords.longitude;
        const message = {lat: lat, lon: lon};
        window.parent.postMessage({type: 'streamlit:setComponentValue', data: message}, '*');
    }
    function showError(error) {
        switch(error.code) {
            case error.PERMISSION_DENIED:
                alert('User denied the request for Geolocation.');
                break;
            case error.POSITION_UNAVAILABLE:
                alert('Location information is unavailable.');
                break;
            case error.TIMEOUT:
                alert('The request to get user location timed out.');
                break;
            case error.UNKNOWN_ERROR:
                alert('An unknown error occurred.');
                break;
        }
    }
    </script>
    """
    components.html(geolocation_html, height=0, width=0)

# Initialize the backend setup
def setup_backend():
    load_dotenv()
    api_key = os.getenv('API_KEY')
    genai.configure(api_key=api_key)

    generation_config = {
        "temperature": 0.1,
        "top_p": 1,
        "top_k": 1,
        "max_output_tokens": 2048,
    }

    safety_settings = [
        {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
        {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
        {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
        {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    ]

    model = genai.GenerativeModel(model_name="gemini-1.0-pro", generation_config=generation_config, safety_settings=safety_settings)
    return model

model = setup_backend()

# Function to get the itinerary based on user input
def get_itinerary(user_location, days, must_go_places, food_preferences, budget):
    prompt = f'''You are a Travel advisor GPT, your task is to give a list of itineraries, based on user inputs like :
City :
User Location :
No of days they are staying :
Food Interests:(List of Cuisines)
Locations user wants to for sure visit :
Budget of the user: (Budget Friendly, No Cost Preference)
if user says “Budget Friendly ” The itineraries should be focused with in 
	-  First preference, save budget 
	- Second preference to Places user want to visit, Popular locations in that city
	- Cover most places they can
if user says “No Cost Preference ” The itineraries should be focused
	- first preference to Places user want to visit, Popular locations in that city
	- Cover most places they can

all itineraies should start from places near user location 
the list of itineraies should go from low budget to high budget 
and every itinerary should cover users must visit places list as 

Output should be a json formatted with a list of 4 itineraries



Inputs :
City : Chicago
User Location : {user_location}
No of days they are staying : {days}
Locations user wants to for sure visit :  [{must_go_places}]
Food Interests: [{food_preferences}] 
Budget: {budget}'''
    convo = model.start_chat(history=[])
    convo.send_message(prompt)
    try:
        # Check if the last response is valid
        response = convo.last.text
    except ValueError as e:
        # Handle the case where the response was blocked
        print(e)
        response = "The response was blocked by the model's safety settings."
    return response
# Streamlit app title

logo_path = 'C:/Users/saira/ScarletHacks-1/backend/WhatsApp Image 2024-04-15 at 00.10.16_fce43b06.jpg'  # Change this to the path of your logo

# Display the logo
st.image(logo_path, width=400) 
st.title('Chicago Tourism Itinerary ')

# Embed custom CSS with Streamlit components
# components.html(hide_streamlit_style)

# Define columns for layout
col1, col2 = st.columns([4, 1])

# Location input field
with col1:
    user_location = st.text_input('Enter your location')

# Geolocation button
with col2:
    if st.button('📍', key='get_location'):
        get_location()  # Call the JavaScript function to get the geolocation

# Collect additional user inputs
days = st.number_input('Number of days for tourism', min_value=1, max_value=30)
must_go_places = st.text_input('Must-go places')
food_preferences = st.selectbox(
    'Food Preferences',
    ['Select a Cuisine', 'Indian', 'Mexican', 'Chinese', 'Italian', 'Thai', 'Japanese', 'French', 'Mediterranean', 'Korean']
)
budget = st.radio(
    "Budget for the trip",
    ('Budget Friendly', 'No Cost Preference'),
    key='budget'
)

# Generate itinerary button
if st.button('Generate Itinerary'):
    # Check if the user has selected a cuisine
    if food_preferences != 'Select a Cuisine':
        itinerary = get_itinerary(user_location, days, must_go_places, food_preferences, budget)
        st.text(itinerary)
    else:
        st.error('Please select a food preference.')

