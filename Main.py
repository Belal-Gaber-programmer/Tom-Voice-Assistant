import pyttsx3
import speech_recognition as sr
import datetime
import time
import os
import webbrowser
from requests import get
import wikipedia
import pyjokes
import PyPDF2
import requests
import pyautogui as gui
import operator
from bs4 import BeautifulSoup
from pywikihow import search_wikihow
import psutil
import sys
from geopy.distance import great_circle
from geopy.geocoders import Nominatim
import geocoder
import random
from playsound import playsound
import pywhatkit as kit
from PyQt5 import QtCore , QtWidgets , QtGui
from PyQt5.QtGui import QMovie
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtCore import Qt , QTimer , QTime , QDate
from PyQt5.uic import loadUiType
from fnmatch import translate
from googletrans import Translator
import googletrans
from gtts import gTTS
from time import sleep
from datetime import timedelta
from datetime import datetime
import pywhatkit


for i in range(3):
    a = input("Enter Password to open Tom: ")
    pw_file = open("password.txt","r")
    pw = pw_file.read()
    pw_file.close()
    if (a==pw):
        break
    elif (i==2 and a!=pw):
        exit()

    elif (a!=pw):
        print("Try Again")


engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voices', voices[0].id)
engine.setProperty('rate', 150)

def wish():
    current_time = datetime.now().time()
    morning_start = datetime.strptime("06:00:00", "%H:%M:%S").time()
    afternoon_start = datetime.strptime("12:00:00", "%H:%M:%S").time()
    evening_start = datetime.strptime("17:00:00", "%H:%M:%S").time()
    night_start = datetime.strptime("21:00:00", "%H:%M:%S").time()
    
    if morning_start <= current_time < afternoon_start:
        speak("Good morning!")
    elif afternoon_start <= current_time < evening_start:
        speak("Good afternoon!")
    elif evening_start <= current_time < night_start:
        speak("Good evening!")
    else:
        speak("Good night!")
    speak("Iam Tom, How can I help you")

def speak(audio):
    engine.say(audio)
    print(audio)
    engine.runAndWait()

def takecommands():
    command = sr.Recognizer()
    with sr.Microphone() as mic :
        print("listening....")
        command.adjust_for_ambient_noise(mic)
        command.pause_threshold = 1
        audio = command.listen(mic)
        try:
            print("Recognizing....")
            query = command.recognize_google(audio, language='en-us')
            print(f"you said: {query}")
        except Exception as e:
            speak("sorry, can you say that again")
            return "none"
    return query

def news():
    main_url = 'https://newsapi.org/v2/top-headlines?sources=techcrunch&apikey=bbb9544e6a614fd2b3b0c66477b26d24'

    main_page = requests.get(main_url).json()
    articles = main_page["articles"]
    head = []
    day=["first","second","third","fourth","fifth","sixth","seventh","eighth","ninth","tenth"]
    for ar in articles:
        head.append(ar["title"])
    for i in range (len(day)):
        speak(f"today's {day[i]} news is: {head[i]}")

def pdf_reader():
    speak("please enter the name of the book")
    name = input("Enter the book name:")
    book = open(name,'rb')
    pdfReader = PyPDF2.PdfFileReader(book)
    pages = pdfReader.numPages
    speak(f"total number of pages in this book is {pages}")
    speak("sir please enter the page number I have to read")
    pg = int(input("please enter the page number:"))
    page = pdfReader.getPage(pg)
    text = page.extractText()
    speak(text)

def My_Location():
    ip_add = requests.get('https://api.ipify.org').text
    url = 'https://get.geojs.io/v1/ip/geo/' + ip_add + '.json'
    geo_q = requests.get(url)
    geo_d = geo_q.json()
    country = geo_d['country']
    speak(f"sir, you are now in {country}")

def GoogleMaps(place):
    url_place = "https://www.google.com/maps/place/" + str(place)
    geolocator = Nominatim(user_agent="mygeocoder")
    location = geolocator.geocode(place, addressdetails= True)
    target_latlon = location.latitude , location.longitude
    location = location.raw['address']
    target = {'city' : location.get('city',''),
               'state' : location.get('state',''),
               'country' : location.get('country','')}
    current_loca = geocoder.ip('me')
    current_latlon = current_loca.latlng
    distance = str(great_circle(current_latlon,target_latlon))
    distance = str(distance.split(' ',1)[0])
    distance = round(float(distance),2)
    speak(target)
    speak(f"sir {place} is {distance} Kilometer away from your location")
    webbrowser.open(url=url_place)

def SolarBodies(body):
    url = "https://api.le-systeme-solaire.net/rest/bodies/"
    r = requests.get(url)
    Data = r.json()
    bodies = Data['bodies']
    number = len(bodies)
    url_2 = f"https://api.le-systeme-solaire.net/rest/bodies/{body}"
    rrr = requests.get(url_2)
    Data_2 = rrr.json()
    mass = Data_2['mass']['massValue']
    volume = Data_2['vol']['volValue']
    density = Data_2['density']
    gravity = Data_2['gravity']
    escape = Data_2['escape']

    speak(f"The number of bodies in solar system is: {number}")
    speak(f"The mass of {body} is: {mass}")
    speak(f"The volume of {body} is: {volume}")
    speak(f"The density of {body} is: {density}")
    speak(f"The gravity of {body} is: {gravity}")
    speak(f"The escape velocity of {body} is: {escape}")

Api_key = "4PzSpO8n2gcE2Gmq68ZsYmLjdE2v4XocoZLPwVtt"

def NasaNews(Date):
    speak("Extracting data from Nasa")
    url = "https://api.nasa.gov/planetary/apod?api_key=" + str(Api_key)
    params = {'date':str(Date)}
    r = requests.get(url,params = params)
    Data = r.json()
    info = Data['explanation']
    title = Data['title']
    image_url = Data['url']
    image_r = requests.get(image_url)
    filename = str(Data) + '.jpg'
    with open(filename, 'wb') as f:
        f.write(image_r.content)
    speak(f"Title : {title}")
    speak(f"According to Nasa : {info}")

def Game_play():
    speak("let's play rock paper scissors")
    i = 0
    My_score = 0
    com_score = 0

    while(i<10):
        choose = ("rock","paper","scissors")
        com_choose = random.choice(choose)
        query =takecommands()
        if(query == "Rock"):
            if(com_choose == "rock"):
                speak("rock")
                print(f"score ME:{My_score}  TOM:{com_score}")
                speak("Draw")
            elif(com_choose == "paper"):
                speak("paper")
                com_score += 1
                print(f"score ME:{My_score}  TOM:{com_score}")
                speak("one for me")
            else:
                speak("scissors")
                My_score += 1
                print(f"score ME:{My_score}  TOM:{com_score}")
                speak("one for you")

        elif(query == "paper"):
            if (com_choose == "rock"):
                speak("rock")
                My_score += 1
                print(f"score ME:{My_score}  TOM:{com_score}")
                speak("one for you")
            elif (com_choose == "paper"):
                speak("paper")
                print(f"score ME:{My_score}  TOM:{com_score}")
                speak("Draw")
            else:
                speak("scissors")
                com_score += 1
                print(f"score ME:{My_score}  TOM:{com_score}")
                speak("one for me")

        else:
            if (com_choose == "rock"):
                speak("rock")
                com_score += 1
                print(f"score ME:{My_score}  TOM:{com_score}")
                speak("one for me")
            elif (com_choose == "paper"):
                speak("paper")
                My_score += 1
                print(f"score ME:{My_score}  TOM:{com_score}")
                speak("one for you")
            else:
                speak("scissors")
                print(f"score ME:{My_score}  TOM:{com_score}")
                speak("Draw")
        i += 1
        print(f"score ME:{My_score}  TOM:{com_score}")

def YoutubeSearch(term):
    result = "https://www.youtube.com/results?search_query=" + term
    webbrowser.open(result)
    speak("This Is What I Found For Your Search")
    kit.playonyt(term)
    speak("This May Also Help You Sir")

def GoogleSearch(term):
    query = term.replace("Tom","")
    query = term.replace("what is","")
    query = term.replace("how to","")
    query = term.replace("what is","")
    query = term.replace(" ","")
    query = term.replace("what do you mean by","")
    writeab = str(query)

    ooooo = open("C:\\Users\\elkrnk2022\\Desktop\\Tom\\search.txt",'a')
    ooooo.write(writeab)
    ooooo.close()

    Query = str(term)
    kit.search(Query)
    if "how to" in Query:
        max_result = 1
        how_to_func = search_wikihow(query=Query,max_results=max_result)
        assert len(how_to_func) == 1
        how_to_func[0].print()
        speak(how_to_func[0].summary)

    else:
        search = wikipedia.summary(Query,2)
        speak(f"According to your search: {search} ")

strTime = int(datetime.now().strftime("%H"))
update = int((datetime.now()+timedelta(minutes = 2)).strftime("%M"))

def sendMessage():
    speak("Who do you want to message")
    a = int(input("1-Belal, 2-Dad, 3-Mom (Enter numbers only):"))
    if a == 1:
        speak("What is the message, sir")
        message = str(input("Enter the message: "))
        pywhatkit.sendwhatmsg("+201279924644",message,time_hour=strTime,time_min=update)
    elif a==2:
        speak("What is the message, sir")
        message = str(input("Enter the message: "))
        pywhatkit.sendwhatmsg("+201228213138",message,time_hour=strTime,time_min=update)
    elif a==3:
        speak("What is the message, sir")
        message = str(input("Enter the message: "))
        pywhatkit.sendwhatmsg("+201285014494",message,time_hour=strTime,time_min=update)
        
def TaskExe():
    while True:

        query = takecommands()

        if "how are you" in query:
            speak("Iam fine sir")

        elif "hi" in query or "hello" in query:
            speak("Hi sir, how can I help you today?")

        elif "change password" in query:
            speak("Please enter your new password")
            new_pw = input("Enter the new password\n")
            new_password = open("password.txt", "w")
            new_password.write(new_pw)
            new_password.close()
            speak("Done sir")
            speak(f"Your new password is{new_pw}")

        elif "are you ready" in query:
            speak("Yes sir, I am ready at any time")

        elif "open Notepad" in query or "open Note" in query:
            speak("Ok,sir")
            time.sleep(1)
            npath = "C:\\Windows\\system32\\notepad.exe"
            os.startfile(npath)

        elif "open Google" in query:
            speak("Ok,sir")
            time.sleep(1)
            webbrowser.open_new_tab('https://www.google.com')

        elif "open Instagram" in query or "open insta" in query:
            webbrowser.open_new_tab('https://www.instagram.com')

        elif "open tiktok" in query or "open tick" in query:
            webbrowser.open_new_tab('https://www.tiktok.com')

        elif "open Twitter" in query or "open tweet" in query:
            webbrowser.open_new_tab('https://www.twitter.com')

        elif "open Facebook" in query or "open face" in query:
            webbrowser.open_new_tab('https://www.facebook.com')

        elif "open Gmail" in query:
            webbrowser.open_new_tab('https://accounts.google.com/signin/v2/identifier?hl=ar&continue=https%3A%2F%2Fmail.google.com&service=mail&ec=GAlAFw&flowName=GlifWebSignIn&flowEntry=AddSession')

        elif "open YouTube" in query or "open the red program" in query:
            webbrowser.open_new_tab('https://www.youtube.com/')

        elif "find my IP address" in query or "find IP address" in query or "tell me the IP address" in query:
            ip = get('https://api.ipify.org').text
            speak(f"your IP address is {ip}")

        elif "open Pinterest" in query:
            webbrowser.open_new_tab('https://www.pinterest.com')

        elif "convert text to handwriting" in query:
            try:
                speak("what should I write, sir")
                texting = input("plese write here: ")
                speak("Enter the name of the file")
                name = input("Enter the name: ")
                speak("Enter the file extention like .png , .jpg")
                extn = input("Enter the extention: ")
                kit.text_to_handwriting(texting, ("C:\\Users\\elkrnk2022\\Desktop\\")+ name + extn)

            except Exception as e:
                print(e)
                speak("sorry sir, can you say that again")

        elif "open my account on Facebook" in query or "open my face" in query or "open my account on face" in query:
            webbrowser.open_new_tab('https://www.facebook.com/belal.gaber.7393/')

        elif "open my tiktok" in query or "open my account on tiktok" in query :
            webbrowser.open_new_tab('https://www.tiktok.com/@beasty_222')

        elif "open my School page on Facebook" in query or "open my School page on face" in query:
            webbrowser.open_new_tab('https://www.facebook.com/groups/717550595011509')

        elif "open telegram" in query:
            npath = "C:\\Users\\elkrnk2022\\AppData\\Roaming\\Telegram Desktop\\Telegram.exe"
            os.startfile(npath)

        elif "open IQ option" in query:
            npath = "C:\\Program Files (x86)\\IQ Option\\IQ Option.exe"
            os.startfile(npath)

        elif "open Microsoft Edge" in query:
            npath = "C:\\Program Files\\Microsoft\\Edge\\Application\\msedge.exe"
            os.startfile(npath)

        elif "open command prompt" in query or "open CMD" in query:
            os.system("start cmd")

        elif "Wikipedia" in query:
            speak("searching wikipedia.....")
            query = query.replace("wikipedia","")
            results = wikipedia.summary(query, sentences=3)
            speak("acording to wikipedia")
            speak(results)
            print(results)

        elif "play music" in query:
            music_dir = "C:\\Users\\elkrnk2022\\Desktop\\Tom\\dont.mp3"
            songs = os.listdir(music_dir)
            os.startfile(os.path.join(music_dir , songs[0]))

        elif "open my Instagram" in query or "open my insta" in query or "open my account on Instagram" in query or "open my account on insta" in query:
            webbrowser.open_new_tab('https://www.instagram.com/mindmake_444/')

        elif "open my Pinterest" in query or "open my account on Pinterest" in query:
            webbrowser.open_new_tab('https://www.pinterest.com/Belaldesigns/_created/')

        elif "open my channel on youtube" in query or "open my account on youtube" in query:
            webbrowser.open_new_tab('https://www.youtube.com/channel/UCTRLzNFW94cuqpKhxViinfA')

        elif "play songs on YouTube" in query:
            speak("what should I play, sir")
            ytsong = input("Enter the name of the song: ")
            kit.playonyt(ytsong)

        elif "open WhatsApp" in query:
            npath = ('C:\\Users\\elkrnk2022\\AppData\\Local\\WhatsApp\\WhatsApp.exe')
            os.startfile(npath)

        elif "tell me a joke" in query or "tell me joke" in query:
            joke = pyjokes.get_joke('en')
            speak(joke)

        elif "read PDF" in query or "read PDF file" in query:
            pdf_reader()

        elif "tell me the news" in query:
            speak("please wait sir, feteching the latest news")
            news()

        elif "switch the window" in query:
            gui.keyDown("alt")
            gui.press("tab")
            time.sleep(1)
            gui.keyUp("alt")

        elif "calculate" in query or "do some calculations" in query:
            r = sr.Recognizer()
            with sr.Microphone() as mic:
                speak("say what you want to calculate, example: 3 plus 3")
                print("listening....")
                r.adjust_for_ambient_noise(mic)
                audio = r.listen(mic)
            my_string = r.recognize_google(audio)
            print(my_string)
            def get_operator_fn(op):
                return {
                    "+" : operator.add,
                    "-" : operator.sub,
                    "x" : operator.mul,
                    "devided" : operator.__truediv__,
                }[op]
            def eval_binary_expr(op1, oper, op2):
                op1,op2 = int(op1), int(op2)
                return get_operator_fn(oper)(op1, op2)
            speak("your result is: ")
            speak(eval_binary_expr(*(my_string.split())))

        elif "temperature" in query or "what is the temperature" in query:
            speak("What's the city")
            temptext = "temperature"
            search = input("Please enter the name of the city: ") + " " + temptext
            url = f"https://www.google.com/search?q={search}"
            r = requests.get(url)
            data = BeautifulSoup(r.text,"html.parser")
            temp = data.find("div",class_="BNeawe").text
            speak(f"current {search} is {temp} ")

        elif "battery" in query or "how much power left" in query or "how much power do we have" in query or "how much power we have" in query:
            battery = psutil.sensors_battery()
            percentage = battery.percent
            speak(f"sir our system have {percentage} percent battery")

        elif "volume up" in query or "increase" in query:
            speak("ok,sir")
            gui.press("volumeup")

        elif "volume down" in query or "decrease" in query:
            speak("ok,sir")
            gui.press("volumedown")

        elif "volume mute" in query or "mute" in query:
            speak("ok,sir")
            gui.press("volumemute")

        elif "close the program" in query or "close program" in query or "goodbye" in query or "see you" in query or "you can sleep now" in query:
            speak("Thanks for using me sir, have a good day")
            sys.exit()

        elif "space news" in query:
            speak("please sir tell me the date to extracting data")
            Date = input("Enter the date: ")
            NasaNews(Date)

        elif "alarm" in query:
            speak("please enter the time")
            Time = input("Enter the time:")
            while True:
                Time_Ac = datetime.datetime.now()
                now = Time_Ac.strftime("%H:%M:%S")
                if now == Time:
                    speak("it's time to wake up sir!")
                    playsound("C:\\Users\\elkrnk2022\\Desktop\\Tom\\tom.mp3")
                    playsound("C:\\Users\\elkrnk2022\\Desktop\\Tom\\tom.mp3")
                    playsound("C:\\Users\\elkrnk2022\\Desktop\\Tom\\tom.mp3")
                    playsound("C:\\Users\\elkrnk2022\\Desktop\\Tom\\tom.mp3")
                    playsound("C:\\Users\\elkrnk2022\\Desktop\\Tom\\tom.mp3")
                    playsound("C:\\Users\\elkrnk2022\\Desktop\\Tom\\tom.mp3")
                    playsound("C:\\Users\\elkrnk2022\\Desktop\\Tom\\tom.mp3")
                    playsound("C:\\Users\\elkrnk2022\\Desktop\\Tom\\tom.mp3")
                    playsound("C:\\Users\\elkrnk2022\\Desktop\\Tom\\tom.mp3")
                    playsound("C:\\Users\\elkrnk2022\\Desktop\\Tom\\tom.mp3")
                    playsound("C:\\Users\\elkrnk2022\\Desktop\\Tom\\tom.mp3")
                    playsound("C:\\Users\\elkrnk2022\\Desktop\\Tom\\tom.mp3")
                    playsound("C:\\Users\\elkrnk2022\\Desktop\\Tom\\tom.mp3")
                    playsound("C:\\Users\\elkrnk2022\\Desktop\\Tom\\tom.mp3")
                    playsound("C:\\Users\\elkrnk2022\\Desktop\\Tom\\tom.mp3")
                    playsound("C:\\Users\\elkrnk2022\\Desktop\\Tom\\tom.mp3")
                    playsound("C:\\Users\\elkrnk2022\\Desktop\\Tom\\tom.mp3")
                    playsound("C:\\Users\\elkrnk2022\\Desktop\\Tom\\tom.mp3")
                    playsound("C:\\Users\\elkrnk2022\\Desktop\\Tom\\tom.mp3")
                    playsound("C:\\Users\\elkrnk2022\\Desktop\\Tom\\tom.mp3")
                elif now > Time:
                    break

        elif "how to" in query:
            speak("Getting data from the internet")
            op = query.replace("Tom","")
            max_result = 1
            how_to_func = search_wikihow(op,max_result)
            assert len(how_to_func) == 1
            how_to_func[0].print()
            speak(how_to_func[0].summary)

        elif "my location" in query:
            My_Location()

        elif "search on Google Maps" in query or "Google Maps" in query:
            speak("please tell me What should I search")
            place = takecommands()
            url_place = "https://www.google.com/maps/place/" + str(place)
            webbrowser.open(url=url_place)

        elif "where is" in query:
            place = query.replace("where is","")
            place = place.replace("Tom" ,"")
            GoogleMaps(place)

        elif "remember that" in query:
            rememberMsg = query.replace("remember that","")
            rememberMsg = query.replace("Tom","")
            speak("you tell me remind you that:"+rememberMsg)
            remember = open('data.txt','w')
            remember.write(rememberMsg)
            remember.close()

        elif "what do you remember" in query:
            remember = open('data.txt','r')
            speak("you tell me that:" + remember.read())

        elif "solar system" in query or "solar bodies" in query or "solar body" in query:
            speak("please sir tell me the name of a solar body to getting data")
            bod = input("Enter the body name: ")
            body = bod.replace(" ","")
            body = body.replace(" ", "")
            Body = str(body)
            SolarBodies(body=Body)

        elif "the time" in query or "time" in query:
            strTime = datetime.datetime.now().strftime("%H:%M")
            speak(f"Sir, the time is: {strTime}")

        elif "play a game" in query or "game" in query:
            Game_play()

        elif "shut down" in query:
            speak("Ok sir, I will shutdown the system now")
            os.startfile("C:\\Windows\\System32\\shutdown.exe")

        elif "sleep" in query:
            speak("Ok sir, I will sleep the system now")
            os.startfile("C:\\Windows\\System32\\rundll32.exe")

        elif "restart" in query:
            speak("Ok sir, I will restart the system")
            os.startfile("C:\\Windows\\System32\\shutdown.exe")

        elif "YouTube search" in query or "search on youtube" in query:
            Query = query.replace("Tom","")
            query = Query.replace("youtube search","")
            YoutubeSearch(query)

        elif "Google search" in query or "search on google" in query:
            GoogleSearch(query)

        elif "WhatsApp" in query or "Whatsapp message" in query:
            sendMessage()
            
        elif "what can you do" in query:        
            speak("I can open facebook")
            speak("I can open tiktok")
            speak("I can open instagram")
            speak("I can open pinterest")
            speak("I can open twitter")
            speak("I can open G-mail")
            speak("I can open youtube")
            speak("I can open your account on facebook")
            speak("I can open your account on instagram")
            speak("I can open your account on tiktok")
            speak("I can open your account on pinterest")
            speak("I can open your channel on youtube")
            speak("I can open your account on G-mail")
            speak("I can open your school page on facebook")
            speak("I can open CMD")
            speak("I can open IQ option Trading broker")
            speak("I can open microsoft edge")
            speak("I can open notepad")
            speak("I can open google")
            speak("I can convert text to handwriting")
            speak("I can send a whatsapp messages automaticly")
            speak("I can find your IP address")
            speak("I can play music")
            speak("I can change the password")
            speak("I can tell you the time")
            speak("I can play with you")
            speak("I can tell you the daily news")
            speak("I can find your location")
            speak("I can tell you how to do or make anything")
            speak("I can tell you the space news")
            speak("I can tell you informations about any solar body")
            speak("I can set alarm for you")
            speak("I can remember anything you say to me")
            speak("I can find the location of any place on the Earth")
            speak("I can find the distance between any place and your location")
            speak("I can increase the volume")
            speak("I can decrease the volume")
            speak("I can mute the volume")
            speak("I can tell you the temperature")
            speak("I can calculate any calculations")
            speak("I can switch the window")
            speak("I can read any PDF files")
            speak("I can tell you jokes")
            speak("I can play any song on youtube")
            speak("I can tell you any information about anything")
            speak("I can shutdown the system")
            speak("I can sleep the system")
            speak("I can restart the system")
            speak("I can do a google search direct from me")
            speak("I can do youtube search direct from me")
            speak("I can check the battery percentage for laptops")
            speak("I can control your home like turn on and turn off the light but this feature is not avaiable now")
            speak("I can control your car like open and close the windows but also this feature is not avaiable now")
wish()