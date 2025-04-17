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

from datetime import date, datetime


def get_cycle_info():
    "Accepts user input for the start date of the last period, and typical duration of the period."
    while True:
        start_date_str = input("Enter the first day of your last period (YYYY-MM-DD): ")
        try:
            cycle_start_date = datetime.strptime(start_date_str, "%Y-%m-%d").date()
            today = date.today()  # Get the current date dynamically

            if cycle_start_date > today:
                print("The start date cannot be in the future. Please enter a valid past or current date.")
            else:
                break
        except ValueError:
            print("Invalid date format. Please use YYYY-MM-DD.")


    while True:
        duration_str = input("Enter the typical duration of your period in days (e.g., 5): ")
        try:
            period_duration = int(duration_str)
            if period_duration > 0:
                return cycle_start_date, period_duration
            else:
                print("Period duration must be a positive number.")
        except ValueError:
            print("Invalid input. Please enter a number for the duration.")


# def calculate_cycle_day(last_period_date):
#     """
#     Calculate the current cycle day based on the last period start date.
#     """
#     today = date.today()
#     delta = today - last_period_date
#     return delta.days + 1  # Cycle day starts at 1



# def get_cycle_phase(cycle_day):
#     """
#     Determine the cycle phase based on the current cycle day.
#     """
#     if 1 <= cycle_day <= 5:
#         return "Menstruation"
#     elif 6 <= cycle_day <= 13:
#         return "Follicular"
#     elif 14 <= cycle_day <= 20:
#         return "Ovulation"
#     elif 21 <= cycle_day <= 28:
#         return "Luteal"
#     else:
#         return "Unknown Phase"


# def map_phase_to_mood(cycle_phase):
#     """
#     Map the cycle phase to a predicted mood or list of moods.
#     """
#     phase_to_mood = {
#         "Menstruation": ["Tired", "Reflective"],
#         "Follicular": ["Energetic", "Optimistic"],
#         "Ovulation": ["Confident", "Social"],
#         "Luteal": ["Irritable", "Introspective"]
#     }
#     return phase_to_mood.get(cycle_phase, "Unknown Mood")


# def recommend_playlist(predicted_mood):
#     """
#     Recommend a Spotify playlist URL based on the predicted mood.
#     """
#     mood_to_playlist = {
#         "Tired": "https://open.spotify.com/playlist/tired_playlist",
#         "Reflective": "https://open.spotify.com/playlist/reflective_playlist",
#         "Energetic": "https://open.spotify.com/playlist/energetic_playlist",
#         "Optimistic": "https://open.spotify.com/playlist/optimistic_playlist",
#         "Confident": "https://open.spotify.com/playlist/confident_playlist",
#         "Social": "https://open.spotify.com/playlist/social_playlist",
#         "Irritable": "https://open.spotify.com/playlist/irritable_playlist",
#         "Introspective": "https://open.spotify.com/playlist/introspective_playlist"
#     }
#     if isinstance(predicted_mood, list):
#         return [mood_to_playlist.get(mood, "https://open.spotify.com/playlist/default_playlist") for mood in predicted_mood]
#     return mood_to_playlist.get(predicted_mood, "https://open.spotify.com/playlist/default_playlist")



if __name__ == "__main__":
    print("Welcome to Siren - Your Cycle-Aware Music Companion!")
    start_date, period_duration = get_cycle_info()
    print(f"Your typical period duration is {period_duration} days.")
    print(f"Your last period started on {start_date}.")
    
    # cycle_day = calculate_cycle_day(start_date)
    # print(f"\nBased on your last period starting on {start_date}, today is day {cycle_day} of your cycle.")

    # cycle_phase = get_cycle_phase(cycle_day, period_duration)
    # predicted_mood = map_phase_to_mood(cycle_phase)
    # playlist_link = recommend_playlist(predicted_mood)

    # print(f"Your predicted mood for the {cycle_phase} phase is: {predicted_mood}")
    # print(f"Here's a Spotify playlist to match: {playlist_link}")