import datetime
import os
import subprocess
from time import sleep
import time
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles  # <-- move this import to top
import requests
import webbrowser
import pyautogui
from datetime import datetime
from bs4 import BeautifulSoup
import psutil
from keyboard import press_and_release
import pyjokes
from pywikihow import search_wikihow


from devil_voice_assistant import ChromeAuto, GoogleMapsDist, YouTubeAuto, helping_mode, takecommand, get_ai_response, speak, SpeedTest

# ✅ Create the FastAPI app
app = FastAPI()



# ✅ Enable CORS (optional for dev)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Define routes
@app.get("/voice-chat")
def voice_chat():
    battery=psutil.sensors_battery()
    percentage=battery.percent

    if percentage >=15 and percentage <40:
        speak("we don't have enough power to work,please connect to charging ")
    elif percentage <=15:
        speak("we have very low power, please connect to charging the system will shutdown soon") 

    while True: 
        speak("Please let know new command you want perform on laptop")      
        query = takecommand().lower()

        if query == "none":
            speak("Sorry, I didn't understand.")
            continue

        if "exit" in query or "quit" in query or "stop voice" in query:
            speak("Exiting voice control mode.")
            break

        if "open youtube" in query:    
            YouTubeAuto()
            continue
        elif "find the distance" in query:
            words = query.split()
            
            # Try to extract destination from the command directly
            destination = None
            for i in range(len(words)):
                if words[i] == "distance" and i + 1 < len(words):
                    destination = " ".join(words[i + 1:])
                    break

            # If not provided directly, ask the user
            if not destination:
                speak("For which country or place?")
                destination = takecommand()
                

            if destination and destination.lower() != "none":
                result=GoogleMapsDist(destination)

                return {
                "spoken_query": f"Find distance to {destination}",
                "ai_reply": result
                }
            else:
                speak("Sorry, I didn't get the location.")
            
        elif "find my location" in query:
            speak("Wait sir, let me check.")
            
            speak("Trying to find your location using Google Maps.")
            
            # Get public IP
            ipAdd = requests.get("https://api.ipify.org").text
            
            # Get geo info from IP
            url = f"https://get.geojs.io/v1/ip/geo/{ipAdd}.json"
            geo_response = requests.get(url)
            geo_data = geo_response.json()

            timezone = geo_data.get('timezone', 'Unknown timezone')
            region = geo_data.get('region', 'Unknown region')
            country = geo_data.get('country', 'Unknown country')

            # Speak location
            speak(f"Sir, I think we are in {region}, which is a state in {country}. This is part of the {timezone} timezone.")

            # Optional: Open location in Google Maps (replace with dynamic lat/lon if needed)
            maps_url = f"https://www.google.com/maps?q={region}"
            webbrowser.open(maps_url)
            
            sleep(5)
        elif "search" in query or "chat gpt" in query:
            try:
                ai_reply = get_ai_response(query)
            except Exception as e:
                return {
                    "spoken_query": query,
                    "ai_reply": f"Error occurred: {str(e)}"
                }
            return {
                "spoken_query": query,
                "ai_reply": ai_reply
            }

        elif "take screenshot" in query or "take a screenshot" in query:
            speak("please sir hold the screen for few second , i am taking screenshot ")
            timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            filename = f"screenshot_{timestamp}.png"
            img = pyautogui.screenshot()
            img.save(filename)
            speak(f"I am done, sir. The screenshot is saved as {filename}")
        
        elif "remember that" in query:
            remember_msg = query.replace("remember that", "").strip()

            if remember_msg:
                speak(f"You told me to remember: {remember_msg}")
                try:
                    with open("data.txt", "w") as remember_file:
                        remember_file.write(remember_msg)
                except Exception as e:
                    speak("Sorry, I couldn't save that. Something went wrong.")
                    print("Error saving memory:", e)
            else:
                speak("You didn't tell me what to remember.")

        elif "what do you remember" in query or "any reminder" in query:
            remeber=open("data.txt","r")
            data=remeber.read()
            print(data)
            speak(f"you tell me that {data}")

        elif "how much power left" in query or "how much power we have" in query or "battery" in query:
            battery=psutil.sensors_battery()
            percentage=battery.percent
            speak(f"sir our system have {percentage} percent battery") 
            if percentage >= 75:
                speak(f"that enough power to continue our work")  
            elif percentage >=40 and percentage < 75:
                speak("we should connect our system to charging point to charge our battery")
            elif percentage >=15 and percentage <40:
                speak("we don't have enough power to work,please connect to charging ")
            elif percentage <=15:
                speak("we have very low power, please connect to charging the system will shutdown soon")    
        
        elif "open camera" in query or "take a photo" in query or "click a photo" in query:
            speak("Opening camera. Please hold steady.")
            os.system("start microsoft.windows.camera:")
            time.sleep(2)  # Wait for camera to open
            speak("Taking a photo now.")
            press_and_release("space")
            time.sleep(2)
            speak("Photo taken. Say 'close camera' if you want to exit.")
            confirm=takecommand()
            if "close camera" in confirm:
                speak("Closing camera.")
                os.system("taskkill /F /IM WindowsCamera.exe")
            else:
                speak("ok keeping camera open")
            
        elif "close camera" in query:
            speak("Closing camera.")
            os.system("taskkill /F /IM WindowsCamera.exe")
        
        elif "sound please" in query:
            pyautogui.press("volumeup")

        elif "sound down" in query:
            pyautogui.press("volumedown")

        elif "mute" in query:
            pyautogui.press("volumemute")
        
        elif "check net" in query or "check net speed" in query:
            text=SpeedTest()
            speak(text)
            return {
                "spoken_query": "here is net speed and upload speed",
                "ai_reply": text
                }

        elif "tell me a joke" in query:
            joke=pyjokes.get_joke()
            speak(joke)
            return {
                "spoken_query": "here is jokes",
                "ai_reply": joke
                }
        
        elif  "open notepad" in query:
            speak("please notepad is opening")
            npath="C:\\WINDOWS\\system32\\notepad.exe"
            os.startfile(npath)
            
        elif "close notepad" in query:
            speak("okay sir closing notepad")
            os.system("taskkill /f /im notepad.exe")
    
        elif "open command prompt" in query:
            speak("please command prompt is opening")
            npath="C:\\WINDOWS\\system32\\cmd"
            os.startfile(npath)

        elif "close command prompt" in query:
            speak("okay sir closing command prompt")
            os.system("taskkill /f /im cmd.exe")
        elif "have problem" in query or "in problem" in query:
            speak("helping mode is active")
            s=0
            while s<3:
                speak("please tell me your problem")
                how=takecommand()
                
                if "no" in how or "close" in how:
                    speak("okay sir,closing helping mode")
                    break
                else:
                    max_results=1
                    how_to=search_wikihow(how,max_results)
                    assert len(how_to)==1
                    how_to[0].print()
                    # speak(how_to[0].summary)
                    s+=1
            speak("ok sir, now it time to close helping mode")
            
        elif "open google" in query:
            webbrowser.open("https://www.google.com")
            time.sleep(8)
            # speak("which task you want in chrome")
            ChromeAuto()  
        else:       
            speak("Okay, no command was executed.")
            continue
        sleep(3)


@app.post("/text-chat")
async def text_chat(request: Request):
    body = await request.json()
    query = body.get("query", "").strip().lower()

    if not query:
        return {
            "spoken_query": "",
            "ai_reply": "Please enter a valid message."
        }

    if "stop" in query or "exit" in query:
        speak("Stopping assistant. Goodbye!")
        os._exit(0)

    if "open youtube" in query:
        YouTubeAuto()
        return {
            "spoken_query": query,
            "ai_reply": "Entered YouTube mode. Say 'exit' to stop."
        }
    

    try:
        ai_reply = get_ai_response(query)
    except Exception as e:
        return {
            "spoken_query": query,
            "ai_reply": f"Error occurred: {str(e)}"
        }

    return {
        "spoken_query": query,
        "ai_reply": ai_reply
    }


# ✅ Mount the static folder for frontend
app.mount("/", StaticFiles(directory="static", html=True), name="static")
