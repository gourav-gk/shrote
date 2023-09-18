import speech_recognition as sr
from gtts import gTTS
import os
from translate import Translator
from playsound import playsound
import webbrowser
from googletrans import Translator as gt
import openai
import wikipedia
import pyjokes
import requests
import spacy
from bardapi import BardCookies
import object_model as oj
import sms

cookie_dict = {
    "__Secure-1PSID": "bAj0VRACzUfA39PRAyRcAJIkMQKWJMWtE4xszYlHpUFXydcQ52npIhRyLuZt14rjYczvwQ.",
    "__Secure-1PSIDTS": "sidts-CjIB3e41hQpXwTtBOOwrF-bFy1yuwJRErBckJkmyj1DPrt1q2w7pfJ6G9-0cADOxkaslxRAA",
    # Any cookie values you want to pass session object.
}

nlp = spacy.load("en_core_web_sm")

# Specify the browser to use (in this case, "chrome")
chrome_path = "C:/Program Files (x86)/Google/Chrome/Application/chrome.exe"  # Change this to your Chrome executable path

# Set the web browser to use Google Chrome
webbrowser.register('chrome', None, webbrowser.BackgroundBrowser(chrome_path))

browser = webbrowser.get('chrome')

# Initialize the recognizer
recognizer = sr.Recognizer()
translator_to_hindi = Translator(to_lang='hi')  # Set the target language to Hindi ('hi')
translator_to_english = Translator(to_lang='en')  # Set the target language to English ('en')

#NLP




# weather
def weather(city):
    url = "https://weatherapi-com.p.rapidapi.com/current.json"
    querystring = {"q": city}
    headers = {
        "X-RapidAPI-Key": "0a1b37bbf1msha49a8f7193eec5ap1ff9acjsn0e816a3e8764",
        "X-RapidAPI-Host": "weatherapi-com.p.rapidapi.com"
    }
    response = requests.get(url, headers=headers, params=querystring).json()
    response = "The weather condition in "+city+" is "+response['current']['condition']['text']+" and temprature is "+str(response['current']['temp_c'])+"degree celcius"
    return response



# google trans

def translate_text(text, target_language):
    translator = gt()
    translated = translator.translate(text, dest=target_language)
    return translated.text

# Function to speak a given text in a specified language
def speak(text, lang='en'):
    tts = gTTS(text=text, lang=lang)
    tts.save("output.mp3")
    #os.system("mpg321 output.mp3")  # You may need to adjust this command based on your OS and audio player
    playsound('output.mp3')



# Function to handle voice commands
def city(translated_command):
    # Sample sentence
    sentence = translated_command

    # Process the sentence using spaCy
    doc = nlp(sentence)

    # Extract state names (GPE - Geopolitical Entity) from the sentence
    state_names = []
    for ent in doc.ents:
        if ent.label_ == "GPE":  # Check if the entity is a geopolitical entity (e.g., state)
            state_names.append(ent.text)

    # Print the recognized state names
    return state_names

def bard_promt(prompt):
    bard = BardCookies(cookie_dict=cookie_dict)
    return bard.get_answer(prompt)['content'][:500]


def process_command(command, target_language='hi'):  # Set the target language to Hindi ('hi')
    try:
        #translation = translator_to_english.translate(command)
        translated_command = command.lower()
        print(translated_command)

        if "hello" in translated_command:
            #words = translated_command.split()
            response = "Hi, i am source. how can i help you"
        elif "who are you" in translated_command:
            response = "Greetings to all! I am source, an AI activated by voice commands. My abilities include comprehending human language, executing tasks, and offering assistance. My primary purpose is to provide accurate guidance and remove obstacles for individuals who may have visual or auditory impairments."
        elif "time" in translated_command:
            from datetime import datetime
            current_time = datetime.now().strftime("%H:%M:%S")
            response = f"The current time is {current_time}."
        elif "open camera" in translated_command:
            codepath="C:\\Users\\shash\\Desktop\\camera"
            os.startfile(codepath)
        elif "youtube" in translated_command:
            response = "Opening Youtube."
            browser.open("youtube.com")
        elif "stop" in translated_command:
            response = "ok listening stopped"
            exit(1)
        elif "who is" in translated_command:
            name = command.replace('who is', '')
            info = wikipedia.summary(name, 1)
            response = info[:500]
        elif "joke" in translated_command:
            response = pyjokes.get_joke()
        elif "weather" in translated_command or "season" in translated_command:
            cityname = city(translated_command)
            if cityname:
                response = str(weather(cityname[0]))
            else:
                response = bard_promt(translated_command)
        elif "front" in translated_command:
            response = oj.detect()
            print(response)
        elif "help" in translated_command:
            sms.send()
            response = "Help request is been sent, please be safe until someone reaches for help"
        else:
            # Send the query to ai for a concise answer
            response = bard_promt(translated_command)

            '''chatgpt_response = openai.Completion.create(
                engine="text-davinci-002",
                prompt=translated_command,
                max_tokens=30,  # Adjust the max tokens as needed for desired conciseness
                n=1,
                stop=None,
                temperature=0.7
            )
            response = chatgpt_response.choices[0].text'''
            #response = "I'm sorry, I don't understand that command."

        # Translate the response to Hindi for speaking
        translated_response = translator_to_hindi.translate(response)
        translated_response = translated_response.replace("*", "")
        speak(translated_response, lang=target_language)
    except Exception as e:
        print(f"Error: {e}")

# Main loop for listening to voice commands
while True:
    with sr.Microphone() as source:
        print("Listening for a command...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    try:
        command = recognizer.recognize_google(audio)  # Recognize Hindi commands
        print(command)
        command = translate_text(command, 'en')
        print("You said (in English): " + command)
        process_command(command, target_language='en')  # Set the target language to Hindi ('hi')
    except sr.UnknownValueError:
        response = "Sorry, I couldn't understand your command."
        print(response)
        response = translator_to_hindi.translate(response)
        speak(response,lang="en")
    except sr.RequestError as e:
        print("Could not request results;{0}".format(e))