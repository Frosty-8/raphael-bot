import pyttsx3
import speech_recognition as sr #type:ignore
import datetime,os,time,webbrowser
import pyautogui 
import sys
import psutil #type:ignore
import json, pickle,random
from tensorflow.keras.models import load_model #type:ignore
from tensorflow.keras.preprocessing.sequence import pad_sequences #type:ignore
import numpy as np
# from elevenlabs import generate , play
# from elevenlabs import set_api_key
# from api_key import api_key_data
# set_api_key(api_key_data)

# def engine_talk(query):
#     audio=generate(
#         text=query,
#         voice='Rachel',
#         model='eleven_monolingual_v2'
#     )
#     play(audio)


with open("intents.json") as file:
    data = json.load(file)

model = load_model("chat_model.h5")

with open("tokenizer.pkl","rb") as f:
    tokenizer = pickle.load(f)

with open("label_encoder.pkl","rb") as encoder_file:
    label_encoder = pickle.load(encoder_file)


def initialize_engine():
    engine = pyttsx3.init("sapi5")
    voices = engine.getProperty("voices")
    engine.setProperty("voice",voices[1].id)
    rate = engine.getProperty("rate")
    engine.setProperty("rate",rate-50)
    volume= engine.getProperty("volume")
    engine.setProperty("volume",volume+0.50)
    return engine

def speak(text):
    engine = initialize_engine()
    print(f"SPEAKING: {text}")  # Debugging print
    engine.say(text)
    engine.runAndWait()
    print("SPEAKING COMPLETE")  # Debugging print


def command():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source,duration=0.5)
        print("Listening.....",end="",flush=True)
        r.pause_threshold=1.0
        r.phrase_threshold=0.3
        r.sample_rate = 48000
        r.dynamic_energy_thresold = True
        r.operation_timeout=5
        r.non_speaking_duration=0.5
        r.dynamic_energy_adjustment=2
        r.energy_threshold = 4000
        r.phrase_time_limit = 10
        # print(sr.Microphone.list_microphone_names())
        audio = r.listen(source)
    try:
        print("\r",end="",flush=True)
        print("Recognizing......",end="",flush=True)
        query = r.recognize_google(audio,language="en-in")
        print("\r",end="",flush=True)
        print(f"User said : {query}\n")
    except Exception as e:
        print("Say that again please")
        return "None"
    return query

def cal_day():
    day = datetime.datetime.today().weekday() + 1
    day_dict={
        1:"Monday",
        2:"Tuesday",
        3:"Wednesday",
        4:"Thursday",
        5:"Friday",
        6:"Saturday",
        7:"Sunday"
    }
    if day in day_dict.keys():
        day_of_week = day_dict[day]
        print(f"Today is {day_of_week}")
    return day_of_week

def wishMe():
    hour = int(datetime.datetime.now().hour)
    t = time.strftime("%I:%M:%p")
    day  = cal_day()

    if(hour>=0) and (hour<=12) and ('AM' in t):
        speak(f" Good Morning Sir, it's {day} and time is {t} ")
    elif(hour>=12) and (hour<=16) and ('PM' in t):
        speak(f" Good Afternoon Sir, it's {day} and time is {t} ")
    else:
        speak(f" Good Evening Sir, it's {day} and time is {t} ")

def social_media(command):
    if 'linkedin' in command:
        speak("Opening your linkedin account")
        webbrowser.open("https://www.linkedin.com/feed/")
    elif 'whatsapp' in command:
        speak("Opening your whatsapp account")
        webbrowser.open("https://web.whatsapp.com/")
    elif 'github' in command:
        speak("Opening your discord account")
        webbrowser.open("https://github.com/Frosty-8")
    elif 'instagram' in command:
        speak("Opening your instagram account")
        webbrowser.open("https://www.instagram.com/")
    else:
        speak("No result found")

def schedule():
    day = cal_day().lower()
    speak(" Boss today's schedule is  ")
    week={
        "monday":"Boss,from 9:00 to 10:00 am you have a football match",
        "tuesday":"Boss,from 9:00 to 10:00 am you have a football match",
        "wednesday":"Boss,from 9:00 to 10:00 am you have a football match",
        "thursday":"Boss,from 9:00 to 10:00 am you have a football match",
        "friday":"Boss,from 9:00 to 10:00 am you have a football match",
        "saturday":"Boss,from 9:00 to 10:00 am you have a football match",
        "sunday":"Boss,from 9:00 to 10:00 am you have a football match"
    }
    if day in week.keys():
        speak(week[day])


def openApp(command):
    if 'calculator' in command:
        speak("Opening calculator")
        os.startfile("C:\\Windows\\System32\\calc.exe")
    if 'notepad' in command:
        speak("Opening notepad")
        os.startfile("C:\\Windows\\System32\\notepad.exe")
    if 'paint' in command:
        speak("Opening paint")
        os.startfile("C:\\Windows\\System32\\paint.exe")

def closeApp(command):
    if 'calculator' in command:
        speak("Closing calculator")
        os.system("taskkill /f /im calc.exe")
    if 'notepad' in command:
        speak("Closing notepad")
        os.system("taskkill /f /im notepad.exe")
    if 'paint' in command:
        speak("Closing paint")
        os.system("taskkill /f /im paint.exe")

def browsing(query):
    if 'google' in query:
        speak("Boss, what should I search on Google?")
        s = command().lower()
        search_query = "+".join(s.split())
        webbrowser.open(f"https://www.google.com/search?q={search_query}")


def condition():
    usage = str(psutil.cpu_percent())
    speak(f"CPU is at {usage} percentage ")

    battery = psutil.sensors_battery()
    if battery is None:
        speak("Battery information is not available on this system.")
    else:
        percentage = battery.percent
        speak(f"Boss, our system has {percentage} percent battery.")

        if percentage >= 80:
            speak("Boss, we have enough charge to continue.")
        elif 40 <= percentage <= 75:
            speak("Boss, we should connect our system to a charger soon.")
        else:
            speak("Boss, battery is very low. Please connect to a charger.")

if  __name__ == "__main__":
    wishMe()
    #engine_talk("Allow ")
    while True:
        query = command().lower()
        #query = input("Enter your command-> ")
        if ('linkedin' in query) or ('github' in query) or ('whatsapp' in query) or ('instagram' in query) :
            social_media(query)
        elif("university time table" in query) or ("schedule" in query):
            schedule()
        elif("volume up" in query) or ("increase volume" in query):
            pyautogui.press("volumeup")
            speak("Volume increased")
        elif("volume down" in query) or ("decrease volume" in query):
            pyautogui.press("volumedown")
            speak("Volume decreased")
        elif("volume mute" in query) or ("mute the sound" in query):
            pyautogui.press("volumemute")
            speak("Volume muted")
        elif("open calculator" in query) or ("open notepad" in query) or ("open paint" in query):
            openApp(query)
        elif("close calculator" in query) or ("close notepad" in query) or ("close paint" in query):
            closeApp(query)
        elif ("what" in query) or ("who" in query) or ("how" in query) or ("hi" in query) or ("thanks" in query) or ("hello" in query):
            padded_sequences = pad_sequences(tokenizer.texts_to_sequences([query]), maxlen=20, truncating='post') 
            result = model.predict(padded_sequences)
            tag = label_encoder.inverse_transform([np.argmax(result)])

            for i in data['intents']:
                if i['tag'] == tag:
                    response = np.random.choice(i['responses'])
                    print(response)  # Print response in console
                    speak(response)  # Make the assistant speak

        
        elif("open google" in query) or ("open brave" in query):
            browsing(query)
        elif ("system condition " in query) or ("condition of the system" in query):
            speak("checking the system condition")
            condition()
        elif "exit" in query:
            sys.exit()
# speak("Hello,I am Raphael, your personal assistant, How can I help you ?") 