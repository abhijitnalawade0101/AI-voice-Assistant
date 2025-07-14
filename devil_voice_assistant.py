# devil_voice_assistant.py

import speech_recognition as sr
import pyttsx3
import os
import time
import datetime
from openai import OpenAI
from dotenv import load_dotenv
from keyboard import press, press_and_release
import webbrowser
import speedtest
# location
from geopy.geocoders import Nominatim
from geopy.distance import great_circle
import geocoder

def speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

def takecommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        speak("listening")
        r.pause_threshold = 1
        audio = r.listen(source)
    try:
        print("Recognizing...")
        speak("recognizing")
        query = r.recognize_google(audio, language='en-in')
        print(f"User said: {query}\n")
        speak(f"User said: {query}\n")
    except Exception as e:
        print("Could not understand.")
        return "none"
    return query

def get_ai_response(prompt):
    load_dotenv()
    token = os.environ["GITHUB_TOKEN"]
    endpoint = "https://models.github.ai/inference"
    model = "openai/gpt-4.1"

    client = OpenAI(
        base_url=endpoint,
        api_key=token,
    )

    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt},
        ],
        temperature=1.0,
        top_p=1.0
    )

    answer = response.choices[0].message.content
    return answer

# 🧾 Save history to a file
def save_history(user_input, ai_reply):
    with open("history.log", "a", encoding="utf-8") as f:
        f.write(f"You: {user_input}\nAI: {ai_reply}\n---\n")

# You Tube
def YouTubeAuto():

    speak("You are now in YouTube control mode. Say 'exit' anytime to stop.")
    flag = True

    while flag:
        speak("What command should I perform on YouTube?")
        query = takecommand().lower()

        if "exit" in query or "quit" in query:
            speak("Exiting YouTube control mode.")
            break

        elif "stop" in query or "pause" in query:
            press("k")

        elif "start" in query or "play" in query:
            press("k")

        elif "full screen" in query:
            press("f")

        elif "small screen" in query:
            press("f")

        elif "increase" in query or "speed up" in query:
            press_and_release("shift + period")

        elif "slow down" in query or "decrease" in query:
            press_and_release("shift + comma")

        elif "next video" in query:
            press_and_release("shift + n")

        elif "search" in query:
            search_query = query.replace("search", "").strip().replace(" ", "+")
            webbrowser.open(f"https://www.youtube.com/results?search_query={search_query}")

        elif "mute" in query or "unmute" in query:
            press("m")

        elif "new tab" in query:
            press_and_release("ctrl + t")

        elif "close tab" in query:
            press_and_release("ctrl + w")

        elif "open new window" in query:
            press_and_release("ctrl + n")

        elif "history" in query:
            press_and_release("ctrl + h")

        elif "downloads" in query:
            press_and_release("ctrl + j")

        elif "bookmark" in query:
            press_and_release("ctrl + d")
            press("enter")

        elif "incognito" in query:
            press_and_release("ctrl + shift + n")

        else:
            speak("Sorry, I didn't understand that command on youtube")

        time.sleep(4)


def GoogleMapsDist(Place):
    try:
        url_place = "https://www.google.com/maps/place/" + str(Place)
        geolocator = Nominatim(user_agent="myGeocoder")

        # Get target location
        location = geolocator.geocode(Place, addressdetails=True)
        if location is None:
            speak(f"Sorry, I couldn't find the location '{Place}' on Google Maps.")
            return

        target_latlon = (location.latitude, location.longitude)
        address = location.raw['address']
        target = {
            'city': address.get('city', ""),
            'state': address.get('state', ""),
            'country': address.get('country', "")
        }

        # Get user's current location
        current_loca = geocoder.ip('me')
        current_latlon = current_loca.latlng
        # speak(f"current loacatoion {current_latlon}")
        if current_latlon is None:
            speak("Unable to determine your current location.")
            return

        # Calculate distance
        distance_km = round(great_circle(current_latlon, target_latlon).km, 2)

        # Open map and speak result
        webbrowser.open(url_place)
        text1 = f"{Place} is in {target['city']}, {target['state']}, {target['country']}."
        text2 = f"{Place} is approximately {distance_km} kilometers away from your current location."
        speak(text1)
        speak(text2)

        return text1 + " " + text2

    except Exception as e:
        speak("Something went wrong while trying to find the distance.")
        print(e)
    
def ChromeAuto():
    while True:
        speak("What command should I perform on Chrome?")
        query = takecommand().lower()

        if 'next tab' in query:
            press_and_release('ctrl + tab')
            speak("Switched to the next tab.")

        elif 'close tab' in query:
            press_and_release('ctrl + w')
            speak("Closed the tab.")

        elif 'new tab' in query:
            press_and_release('ctrl + t')
            speak("Opened a new tab")

        elif 'new window' in query:
            press_and_release('ctrl + n')
            speak("Opened a new Chrome window.")

        elif 'history' in query:
            press_and_release('ctrl + h')
            speak("Showing browsing history.")

        elif 'download' in query or 'downloads' in query:
            press_and_release('ctrl + j')
            speak("Opening downloads page.")

        elif 'bookmark' in query:
            press_and_release('ctrl + d')
            press('enter')
            speak("Page bookmarked.")

        elif 'incognito' in query:
            press_and_release('ctrl + shift + n')
            speak("Opened an incognito window.")

        elif "open" in query:
            name = query.replace("open", "").strip()
            if 'youtube' in name:
                webbrowser.open("https://www.youtube.com/")
                speak("Opening YouTube.")
            else:
                url = f"https://www.{name}.com".replace(" ", "")
                webbrowser.open(url)
                speak(f"Opening {name}.")
        
        elif 'search' in query:
            search_term = query.replace("search", "").strip()
            if search_term:
                speak(f"Searching for {search_term} on Google")
                webbrowser.open(f"https://www.google.com/search?q={search_term}")
            else:
                speak("What should I search?")
                new_search = takecommand().lower()
                webbrowser.open(f"https://www.google.com/search?q={new_search}")
            speak("Search complete. Any other command for Chrome?")

        elif "quit" in query or "stop" in query or "exit" in query:
            speak("Exiting Chrome control.")
            break
        else:
            speak("Sorry, I didn't understand that Chrome command.")

def SpeedTest():
    speak("checking speed....")
    speak("wait sir ,it take time to collecting data")
    speed =speedtest.Speedtest()
    upload=speed.upload()
    correct_Up=int(int(upload)/8000000)
    download=speed.download()
    correct_down=int(int(download)/8000000)
    text1=f"Downloading Speed is {correct_down} M B per second"
    text2=f"uploading speed is {correct_Up} M B per second."
    return text1 + " " + text2

def helping_mode():
    speak("Helping mode is active. Please tell me your problem.")
    problem = takecommand()
    how_to = search_wikihow(problem, max_results=1)
    return how_to