"""Core Function Tools for "Siren":

calculate_cycle_day(last_period_date):
Purpose: Takes the user's last period start date as input and calculates the current cycle day.
Input: datetime.date object representing the last period start date.
Output: int representing the current cycle day.

get_cycle_phase(cycle_day):
Purpose: Takes the current cycle day as input and determines the corresponding cycle phase based on a pre-defined model.
Input: int representing the current cycle day.
Output: str representing the cycle phase (e.g., "Menstruation", "Follicular").

map_phase_to_mood(cycle_phase):
Purpose: Takes the cycle phase as input and returns the predicted mood (or a list of potential moods) associated with that phase.
Input: str representing the cycle phase.
Output: str or list of str representing the predicted mood(s).

recommend_playlist(predicted_mood):
Purpose: Takes the predicted mood as input and retrieves a relevant Spotify playlist URL from a pre-defined dictionary.
Input: str representing the predicted mood.
Output: str representing the Spotify playlist URL.

The Overall Flow of the Agent:
The agent will first get the last_period_date from the user.
It will use the calculate_cycle_day function tool to determine the current_cycle_day.
It will then use the get_cycle_phase function tool to get the cycle_phase.
Next, it will use the map_phase_to_mood function tool to get the predicted_mood.
Finally, it will use the recommend_playlist function tool to get the playlist_url based on the predicted_mood.
The agent will then output the playlist_url to the user.

"""  # siren.py

from datetime import date
import random
import streamlit as st

import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv
import os

load_dotenv()

# Initialize Spotipy (you might want to do this globally or within the function)
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=os.environ.get("SPOTIPY_CLIENT_ID"),
                                               client_secret=os.environ.get("SPOTIPY_CLIENT_SECRET"),
                                               redirect_uri=os.environ.get("SPOTIPY_REDIRECT_URI"),
                                               scope="user-read-private playlist-read-collaborative playlist-modify-public"))

# Initialize session state for storing chat history
if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = []

def display_chat_message(role, content):
    with st.chat_message(role):
        st.markdown(content)

def get_cycle_start_date_from_chat():
    display_chat_message("assistant", "Hello! When was the first day of your last period?")
    start_date = st.date_input("Select the start date")
    if start_date:
        today = date.today()
        if start_date > today:
            display_chat_message("assistant", "Hmm, that date seems to be in the future. Could you double-check?")
            return None
        else:
            display_chat_message("user", start_date.strftime("%Y-%m-%d")) # Display selected date in chat
            return start_date
    return None


def get_period_duration_from_chat():
    display_chat_message("assistant", "Got it. And how many days does your period typically last?")
    duration_str = st.chat_input("Your answer (in days)")
    if duration_str:
        try:
            period_duration = int(duration_str)
            if period_duration > 0:
                display_chat_message("user", duration_str)
                return period_duration
            else:
                display_chat_message("assistant", "Period duration must be a positive number.")
                return None
        except ValueError:
            display_chat_message("assistant", "Invalid input. Please enter a number.")
            return None
    return None


def calculate_cycle_day(cycle_start_date):
    """Calculate the current cycle day based on the cycle start date."""
    today = date.today()  # Dynamically get the current date
    delta = today - cycle_start_date
    return delta.days + 1


def get_cycle_phase(cycle_day, period_duration):
    """Determines the current cycle phase based on the cycle day and period duration."""
    if 1 <= cycle_day <= period_duration:
        return "Menstruation"
    elif period_duration < cycle_day <= 13:  # Assuming average follicular phase length
        return "Follicular"
    elif 14 <= cycle_day <= 16:             # Assuming average ovulation window
        return "Ovulation"
    elif 17 <= cycle_day:                   # Any day 17 or later will be considered Luteal
        return "Luteal"
    else:
        return "Unknown" # This should ideally not be reached with valid positive cycle days


def map_phase_to_mood(cycle_phase):
    mood_map = {
        "Menstruation": ["Blue", "Cranky", "Depressed", "Emotional", "Irritated", "Lazy", "Sad", "Sleepy", "Stressed"],
        "Follicular": ["Calm", "Confident", "Excited", "Happy", "Naughty", "Peaceful", "Romantic", "Sexy", "Unfocused"],
        "Ovulation": ["Confident", "Excited", "Happy", "Naughty", "Romantic", "Sexy"],
        "Luteal": ["Angry", "Anxious", "Confused", "Craving", "Frustrated", "Forgetful", "Irritated", "Jealous", "Stressed", "Emotional"],
        "Unknown": ["General"]
    }
    # Randomly select one mood from the list for the given phase
    return random.choice(mood_map.get(cycle_phase, ["General"]))



def recommend_playlist(predicted_mood):
    """Dynamically searches Spotify for a playlist based on the predicted mood."""
    try:
        results = sp.search(q=predicted_mood + str(" playlist"), type='playlist', limit=1) # Search for one relevant playlist
        print(results)
        if results and 'playlists' in results and results['playlists'] and 'items' in results['playlists'] and results['playlists']['items']:
            if results['playlists']['items'][0] and 'external_urls' in results['playlists']['items'][0] and 'spotify' in results['playlists']['items'][0]['external_urls']:
                return results['playlists']['items'][0]['external_urls']['spotify']
            else:
                print(f"Warning: Could not extract Spotify URL for mood: {predicted_mood}")
                return "https://open.spotify.com/"  # Fallback if URL is missing
        else:
            print(f"Warning: No playlists found for mood: {predicted_mood}")
            return "https://open.spotify.com/"  # Fallback if no playlists found
    except Exception as e:
        print(f"Error searching Spotify: {e}")
        return "https://open.spotify.com/"  # Fallback on error
    

if __name__ == "__main__":
    st.title("Siren - Music That Understands Your Flow.")

    cycle_start_date = get_cycle_start_date_from_chat()
    period_duration = None

    if cycle_start_date:
        period_duration = get_period_duration_from_chat()

    if cycle_start_date and period_duration:
        cycle_day = calculate_cycle_day(cycle_start_date)
        cycle_phase = get_cycle_phase(cycle_day, period_duration)
        predicted_mood = map_phase_to_mood(cycle_phase)
        playlist_link = recommend_playlist(predicted_mood)

        st.subheader("Siren's Recommendation:")
        display_chat_message("assistant", f"Based on your cycle, you are in the **{cycle_phase}** phase, and your predicted mood is **{predicted_mood}**.")
        display_chat_message("assistant", f"Here's a Spotify playlist to match: [Listen on Spotify]({playlist_link})")