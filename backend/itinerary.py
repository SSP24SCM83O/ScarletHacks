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
        "temperature": 0.9,
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

the list of itineraies should go from low budget to high budget 
and every itinerary should cover user’s must visit places list as 

Output should be a json formatted with a list of 4 itineraries
itinerary 1 , itinerary 2 , itinerary 3 , itinerary 4
with each itinerary with unique id having details for for each with List of places with 3 food places with food interests near each place, location coordinates for each place , timing of each place and cost of the visit to each place and day to day places should be optimised by travel time

Inputs :
City : Chicago
User Location : {user_location}
No of days they are staying : {days}
Locations user wants to for sure visit :  {must_go_places}
Food Interests: {food_preferences} 
Budget: {budget}'''
    convo = model.start_chat(history=[])
    convo.send_message(prompt)
    return convo.last.text

# Streamlit app title
st.title('Tourism Itinerary Generator for Chicago')

# Embed custom CSS with Streamlit components
components.html(hide_streamlit_style)

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
