import speech_recognition as sr 
import pyttsx3
import openai
import json
openai.api_key = "YOU_KEY"


engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[2].id)

def talk_text(texto):
    engine.say(texto)
    engine.runAndWait()

r = sr.Recognizer()  

def send(text):
        print(text)
        response = openai.Completion.create(
        model="code-davinci-002",
        prompt=text,
        temperature=0,
        max_tokens=100,
        top_p=1.0,
        frequency_penalty=0.0,
        presence_penalty=0.0
        )
        x = json.dumps(response)
        x1 = x.find("\"text\":")
        resu = x[x1+10:len(x)]
        x2 = resu.find("\\n\\n")
        resu = resu[0:x2]
        resu1 = resu.replace('\\u00c1','Á')
        resu1 = resu1.replace('\\u00e1','á')
        resu1 = resu1.replace('\\u00c9','É')
        resu1 = resu1.replace('\\u00e9','é')
        resu1 = resu1.replace('\\u00cd','Í')
        resu1 = resu1.replace('\\u00ed','í')
        resu1 = resu1.replace('\\u00d3','Ó')
        resu1 = resu1.replace('\\u00f3','ó')
        resu1 = resu1.replace('\\u00da','Ú')
        resu1 = resu1.replace('\\u00fa','ú')
        resu1 = resu1.replace('\\u00d1','Ñ')
        resu1 = resu1.replace('\\u00f1','ñ')
        resu1 = resu1.replace('\\u201c','')
        resu1 = resu1.replace('\\u2013','')
        resu1 = resu1.replace('n\\n','')         
        return resu1
while(1):                 
        try: 
            with sr.Microphone() as source: 
                r.adjust_for_ambient_noise(source, duration=0.3) 
                audio = r.listen(source) 
                text = r.recognize_google(audio, language="es-ES")
                text = text.lower()
                text = send("¿" + text + "?")
                print("Hablando: " + text)              
                talk_text(text) 
 
        except sr.RequestError as e: 
            print("Could not request results; {0}".format(e)) 
          
        except sr.UnknownValueError: 
            print("unknown error occured")
