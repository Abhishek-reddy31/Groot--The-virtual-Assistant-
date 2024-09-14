import pyautogui
import time
import pyttsx3
import pywhatkit
import yfinance as yf
import pyjokes
import webbrowser
import datetime
import wikipedia
import speech_recognition as sr
import cv2
import os
import wolframalpha
import subprocess
from ecapture import ecapture as ec
import json
import requests
import threading
import tkinter as tk
from PIL import Image
from PIL import GifImagePlugin
import sys
#modules for volume controlling
#import cv2
import mediapipe as mp
from math import hypot
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
import numpy as np
#for snake game
from turtle import *
from random import randrange
from freegames import square, vector
import pythoncom

#voice/language options
id1 = "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_DAVID_11.0" 
id2 = "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_ZIRA_11.0"

def transform_audio_into_text(label):
    label.config(fg="black")
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.pause_threshold = 0.8
        print("You can now speak")
        #r.adjust_for_ambient_noise(source)
        audio = r.listen(source)


        try:
            request = r.recognize_google(audio, language="en-gb")

            print("you said "+ request)
            return request
        except sr.UnknownValueError:
            print("Didn't understand audio.")
            return "I am still waiting"
        
        except sr.RequestError:
            print("Didn't understand audio. there is no service")
            return "I am still waiting"
        
        except:
            print("Something went wrong")
            return "I am still waiting"

def speak(message):
    engine = pyttsx3.init()
    engine.setProperty('voice',id2)
    engine.say(message)
    engine.runAndWait()

def speak(message,label):
    engine = pyttsx3.init()
    label.config(fg="green")
    engine.setProperty('voice',id2)
    engine.say(message)
    engine.runAndWait()

def ask_day(label):
    #create a variable with today information
    day = datetime.date.today()
    print(day)

    #variable for day of the week
    week_day = day.weekday()
    print(week_day)
    
    #Names of Days
    calendar = {0: 'Monday',
                1: 'Tuesday',
                2: 'Wednesday',
                3: 'Thursday',
                4: 'Friday',
                5: 'Saturday',
                6: 'Sunday'}
    #say the day of the week
    speak(f'Today is {calendar[week_day]}',label)

def wishMe(label):
    hour=datetime.datetime.now().hour
    if hour>=0 and hour<12:
        speak("Hello,Good Morning",label)
        print("Hello,Good Morning")
    elif hour>=12 and hour<18:
        speak("Hello,Good Afternoon",label)
        print("Hello,Good Afternoon")
    else:
        speak("Hello,Good Evening",label)
        print("Hello,Good Evening")

def ask_time(label):
    #Variable with time info
    time = datetime.datetime.now()
    time = f'At this moment it is {time.hour} hours and {time.minute} minutes'
    print(time)

    #say the time
    speak(time,label)

def initial_greeting(label):
    label.config(fg="black")
    # say greeting
    wishMe(label)
    speak("I am Groot. How can I help you?",label)

def volume():
    cap = cv2.VideoCapture(0) 
    mpHands = mp.solutions.hands
    hands = mpHands.Hands()
    mpDraw = mp.solutions.drawing_utils

    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume = cast(interface, POINTER(IAudioEndpointVolume))

    volMin, volMax = volume.GetVolumeRange()[:2]
    while True:
        success, img = cap.read()
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        results = hands.process(imgRGB)

        lmList = []
        if results.multi_hand_landmarks: 
            for handlandmark in results.multi_hand_landmarks:
                for id, lm in enumerate(handlandmark.landmark):
                    h, w, c = img.shape
                    cx, cy = int(lm.x * w), int(lm.y * h)
                    lmList.append([id, cx, cy]) 
                mpDraw.draw_landmarks(img, handlandmark, mpHands.HAND_CONNECTIONS)

        if lmList != []:
            x1, y1 = lmList[4][1], lmList[4][2]
            x2, y2 = lmList[8][1], lmList[8][2]

            cv2.circle(img, (x1, y1), 15, (255, 0, 0), cv2.FILLED)  
            cv2.circle(img, (x2, y2), 15, (255, 0, 0), cv2.FILLED)  

            cv2.line(img, (x1, y1), (x2, y2), (255, 0, 0), 3)
            length = hypot(x2 - x1, y2 - y1)
            vol = np.interp(length, [15, 220], [volMin, volMax])
            print(vol, length)

            volume.SetMasterVolumeLevel(vol, None)  

            cv2.imshow('Image', img) 
            if cv2.waitKey(1) & 0xff == ord('q'): 
                break
def my_assistant():
    #Activate the initial greeting
    root = tk.Tk()
    label = tk.Label(text="🤖",font=("Arial",120,"bold"))
    label.pack()

    threading.Thread(target=main,args=(root,label)).start()
    root.mainloop()

def main(root,label):
    if threading.current_thread().getName != 'MainThread':
        pythoncom.CoInitialize ()
    initial_greeting(label)

    #Cut-off variable
    go_on = True

    #Main loop
    while go_on:
        # Activate microphone and save request
        my_request = transform_audio_into_text(label).lower()

        if 'hey' in my_request or 'hello' in my_request or 'hi' in my_request:
            speak("Hello",label)
            continue

        elif 'open youtube' in my_request:
            speak("Sure, I am opening Youtube",label)
            webbrowser.open('https://www.youtube.com')
            continue

        elif 'open google' in my_request:
            webbrowser.open_new_tab("https://www.google.com")
            speak("Google chrome is open now",label)
            time.sleep(5)

        elif 'open gmail' in my_request:
            webbrowser.open_new_tab("gmail.com")
            speak("Google Mail open now",label)
            time.sleep(5)
        elif 'open browser' in my_request:
            speak("of course, I am on it",label)
            webbrowser.open("https://www.google.com")
            continue
        elif 'open whatsapp' in my_request:
            speak("of course, I am on it",label)
            webbrowser.open("https://web.whatsapp.com")
            continue


        elif 'what day is today' in my_request:
            ask_day(label)
            continue
        elif 'what time it is' in my_request:
            ask_time(label)
            continue


        elif 'wikipedia search for' in my_request:
            speak("I am looking for it",label)
            my_request = my_request.replace('wikipedia search for','')
            answer = wikipedia.summary(my_request, sentences=1)
            speak("According to wikipedia: ",label)
            speak(answer,label)
            continue
        elif 'wikipedia search for' in my_request:
            speak("I am looking for it",label)
            my_request = my_request.replace('wikipedia search for','')
            answer = wikipedia.summary(my_request, sentences=1)
            speak("According to wikipedia: ",label)
            speak(answer,label)
            continue
        #elif 'search for info on' in my_request:
         #   speak("I am looking for it",label)
          #  my_request = my_request.replace('search for info on','')
           # answer = wikipedia.summary(my_request, sentences=1)
            #speak("According to my search: ",label)
            #speak(answer,label)
            #continue
        elif 'search the internet for' in my_request:
            speak('Of course, right now',label)
            my_request = my_request.replace('search the internet for','')
            pywhatkit.search(my_request)
            speak('this is what i found',label)
            continue
        elif 'play' in my_request:
            speak('oh,what a great idea! I will play it right now ',label)
            pywhatkit.playonyt(my_request)
            continue
        elif 'joke' in my_request:
            speak(pyjokes.get_joke(),label)
            continue
        elif 'stock price' in my_request:
            share = my_request.split()[-2].strip()
            portfolio = {'apple': 'APPL',
                         'amazon': 'AMZN',
                         'google': 'GOOGL'}
            try:
                searched_stock = portfolio[share]
                searched_stock = yf.Ticker(searched_stock)
                price = searched_stock.info['regularMarketPrice']
                speak(f'I found It! The price of {share} is {price} ',label)
                continue
            except:
                speak('I am sorry,but I didnot find it',label)
                continue
        
        elif 'news' in my_request:
            news = webbrowser.open_new_tab("https://timesofindia.indiatimes.com/home/headlines")
            speak('Here are some headlines from the Times of India,Happy reading',label)
            time.sleep(6)
        elif "camera" in my_request or "take a photo" in my_request:
            ec.capture(0,"robo camera","C:/Users/Abhishek Reddy/Desktop/GROOT/images/img.jpg")
            time.sleep(5)
            continue
        elif "logoff" in my_request or "signout" in my_request or "shutdown" in my_request:
            speak("Ok , your pc will log off in 10 seconds.make sure you exit from all applications",label)
            subprocess.call(["shutdown", "/l"])
            time.sleep(10)
			
        
        elif "screenshot" in my_request:
            myScreenshot = pyautogui.screenshot()
            myScreenshot.save(r'C:/Users/Abhishek Reddy/Desktop/GROOT/screenshots/screenshot_1.png')
            speak('Done!',label)
        
        elif 'ask' in my_request:
            speak('I can answer to computational and geographical questions  and what question do you want to ask now',label)
            question =transform_audio_into_text(label)
            app_id="TH4LJV-R5R98U5U2H"
            client = wolframalpha.Client('TH4LJV-R5R98U5U2H')
            res = client.query(question)
            answer = next(res.results).text
            speak(answer,label)
            print(answer)

        elif 'who are you' in my_request or 'what can you do' in my_request:
            speak('I am Groot. version 1 point O, your personal assistant. I am programmed to perform minor tasks like'
                  'opening youtube,google chrome, gmail,WhatsApp',label)
            speak('I can also predict time.  control volume of ur pc',label)
            speak('take a screen shot. take a photo',label)
            speak('search wikipedia. Tell a joke if you ar bored',label)
            speak('I can predict weather In different cities, get top headline news from times of india. and you can ask me computational or geographical questions too!',label)
        elif "who made you" in my_request or "who created you" in my_request or "who discovered you" in my_request:
            speak("I was built by My Master",label)
            print("I was built by My Master")
        elif 'thankyou' in my_request or 'thank you' in my_request:
            speak("your most Welcome.",label) 


        elif "weather" in my_request:
            api_key="8ef61edcf1c576d65d836254e11ea420"
            base_url="https://api.openweathermap.org/data/2.5/weather?"
            speak("what is the city name",label)
            city_name = transform_audio_into_text(label)
            complete_url=base_url+"appid="+api_key+"&q="+city_name
            response = requests.get(complete_url)
            x=response.json()
            if x["cod"]!="404":
                y=x["main"]
                current_temperature = y["temp"]
                current_humidiy = y["humidity"]
                z = x["weather"]
                weather_description = z[0]["description"]
                speak(" Temperature in kelvin unit is " +
                      str(current_temperature) +
                      "\n humidity in percentage is " +
                      str(current_humidiy) +
                      "\n description  " +
                      str(weather_description),label)
                print(" Temperature in kelvin unit = " +
                      str(current_temperature) +
                      "\n humidity (in percentage) = " +
                      str(current_humidiy) +
                      "\n description = " +
                      str(weather_description),label)

        elif 'volume' in my_request:
            speak('Sure. You are gonna love this!!',label)
            volume()
        
        elif 'game' in my_request:
            speak('Sure. Opening the snake game.',label)
            os.system('python snake.py')

        elif 'goodbye' in my_request or 'ok bye' in my_request or 'okay bye' in my_request:
            #speaker = pyttsx3.init()
            #speaker.stop()
            my_request = my_request.replace('goodbye','goodbye groot')
            print(my_request)
            speak('Thankyou. I am going to rest. Let me know if you need anything',label)
            label.config(fg="red")
            root.quit()
            #sys.exit()
            break

my_assistant()