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
    prompt = f"Given that the user is in {user_location}, staying for {days} days, wants to visit {must_go_places}, prefers {food_preferences} food, and has a budget of {budget}, generate a suitable tourism itinerary."
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
    user_location = st.text_input('Enter your location', 'Chicago Riverwalk')

# Geolocation button
with col2:
    if st.button('📍', key='get_location'):
        get_location()  # Call the JavaScript function to get the geolocation

# Collect additional user inputs
days = st.number_input('Number of days for tourism', min_value=1, max_value=30, value=3)
must_go_places = st.text_input('Must-go places', 'Navy Pier, Millennium Park')
food_preferences = st.text_input('Food Preferences', 'Local, Italian')
budget = st.text_input('Budget for the trip', '500')

# Generate itinerary button
if st.button('Generate Itinerary'):
    itinerary = get_itinerary(user_location, days, must_go_places, food_preferences, budget)
    st.text(itinerary)











































# import streamlit as st
# from dotenv import load_dotenv
# import os
# import google.generativeai as genai
# import streamlit.components.v1 as components

# # Function to display HTML/JavaScript for geolocation
# def get_location():
#     # HTML to request geolocation and send it back to Streamlit
#     geolocation_html = """
#     <button onclick="getLocation()">Get Location</button>
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
#     return components.html(geolocation_html, height=30)

# # Initialize your backend setup
# def setup_backend():
#     load_dotenv()
#     api_key = os.getenv('API_KEY')
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

#     model = genai.GenerativeModel(model_name="gemini-1.0-pro", generation_config=generation_config, safety_settings=safety_settings)
#     return model

# model = setup_backend()

# def get_itinerary(user_location, days, must_go_places, food_preferences, budget):
#     prompt = f"Given that the user is in {user_location}, staying for {days} days, wants to visit {must_go_places}, prefers {food_preferences} food, and has a budget of {budget}, generate a suitable tourism itinerary."
#     convo = model.start_chat(history=[])
#     convo.send_message(prompt)
#     return convo.last.text

# st.title('Tourism Itinerary Generator for Chicago')

# # Using the function in app and handling the geolocation
# if st.button('Get Current Location'):
#     location = get_location()
#     if location:
#         user_location = f"{location['latitude']}, {location['longitude']}"
#         st.session_state['user_location'] = user_location

# user_location = st.text_input('Enter your location', value=st.session_state.get('user_location', 'Chicago Riverwalk'))

# days = st.number_input('Number of days for tourism', min_value=1, max_value=30, value=3)
# must_go_places = st.text_input('Must-go places', 'Navy Pier, Millennium Park')
# food_preferences = st.text_input('Food Preferences', 'Local, Italian')
# budget = st.text_input('Budget for the trip', '500')

# if st.button('Generate Itinerary'):
#     itinerary = get_itinerary(user_location, days, must_go_places, food_preferences, budget)
#     st.text(itinerary)














