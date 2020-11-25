import pyttsx3
# pip install pyttsx3==2.71

# speechRecognition
import speech_recognition as sr
import datetime

# install via whl download from here 
# https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyaudio
# then pip install downloadedFileName
import pyaudio
import wikipedia
import webbrowser
import os

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
print(voices[0].id)
engine.setProperty('voice',voices[0].id)





def speak(audio):
    engine.say(audio)
    engine.runAndWait()

def wishMe():
    hour=int(datetime.datetime.now().hour)
    if hour>=0 and hour<12:
        speak("Good Morning")
    elif hour>=12 and hour<18:
        speak("Good Afternoon")
    else:
        speak("Good Evening")

    speak("I am Jarvis sir, Please tell me how I may help you")


def takeCommand():

    
    r=sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        audio=r.listen(source)

    try:
        print("Recognizing...")
        query=r.recognize_google(audio,language='en-in')
        print(f"User said:{query}\n")

    except Exception as e:
       # print(e) want to print error then uncomment

        print("Say that again please...")
        return "None"
    return query


if __name__ == "__main__":
    
    wishMe()

    query=takeCommand().lower()

    if 'wikipedia' in query:
        speak('Searching Wikipedia...')
        query=query.replace("Wikipedia","")
        #results=wikipedia.summary(query)
        speak("According to Wikipedia")
        print(wikipedia.summary(query))
        speak(wikipedia.summary(query))

    elif 'open youtube' in query:
        webbrowser.open("youtube.com")
    elif 'open google' in query:
            webbrowser.open("google.com")
    elif 'open stackoverflow' in query:
        webbrowser.open("stackoverflow.com")
    elif 'play music' in query:
        music_dir=input("Enter your song location\n")
        songs=os.listdir(music_dir)
        print(songs)
        os.startfile(os.path.join(music_dir,songs[0]))
    elif 'the time' in query:
        strTime = datetime.datetime.now().strftime("%H:%M:%S")    
        speak(f"Sir, the time is {strTime}")
    elif 'open code' in query:
        j=input("Enter code location")
        codePath = j
        os.startfile(codePath) 
