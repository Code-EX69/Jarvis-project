import speech_recognition as sr
import webbrowser
import pyttsx3
import musiclibraary
import requests
import os
from openai import OpenAI
recognizer =sr.Recognizer()
engine  = pyttsx3.init()
newsapi= "f9e8a2985fc44ebc9cb1337f57d7a0ea"  

def speak(text):
    engine.say(text)
    engine.runAndWait()



def aiProcess(command):
    client = OpenAI(
    base_url="https://api.aimlapi.com/v1",
    api_key="fd9d86fa94ba4e04bfc0bc2c5b80fa09",    
) 
    response = client.chat.completions.create(
        model="openai/gpt-5-1",
        messages=[
            {
                "role": "system",
                "content": "You are an AI assistant who knows everything.",
            },
            {
                "role": "user",
                "content": command
            },
        ],
    )

    message = response.choices[0].message.content

    return message

def processCommand(c):
    if "open google" in c.lower():
        webbrowser.open("https://google.com") 
    elif "open youtube" in c.lower():
        webbrowser.open("https://youtube.com")
    elif"open linkedin" in c.lower():
        webbrowser.open("https://linkedin.com")
    elif c.lower().startswith("play"):
        song=c.lower().split(" ")[1]
        link= musiclibraary.music[song]
        webbrowser.open(link)

    elif "news" in c.lower():
        r=requests.get(f"https://newsapi.org/v2/top-headlines?country=us&apiKey={newsapi}")
        if r.status_code== 200:
            #parse the json response 
            data = r.json()
 
            #Extract the articles 
            articles =data.get('articles',[])

            #print the headlines 
            for article in articles:
                speak(article['title'])
             


    else:
        #Let open ai handle the request
        output = aiProcess(c)
        speak(output)
        pass
     
if __name__ == "__main__":
    speak("Initialising jarvis") 
    while True:
        # Listen for the wake word jarvis 
        #obtain audio from Microphone
        r = sr.Recognizer()
        
        print("Recognising...")
        try:
            with sr.Microphone() as source:
                print("Listening...")
                audio = r.listen(source,timeout=2,phrase_time_limit=1)

            word = r.recognize_google(audio)
            if(word.lower()=="jarvis"):
               speak("yaa")
               #listen for command
               with sr.Microphone() as source:
                    print("Jarvis Active")
                    audio = r.listen(source)
                    command = r.recognize_google(audio)


                    processCommand(command)
        except Exception as e:
            print("Error; {0}".format(e))
        except sr.RequestError as e:
            print("Sphinx error; {0}".format(e))
  