#import library

import speech_recognition as sr
import pyttsx3
from googletrans import Translator, constants
from pprint import pprint
import threading
from gtts import gTTS
import os
from playsound import playsound
import constants    

engine = pyttsx3.init() # object creation
translator = Translator()

def inputAri(code, output, outputCount):
    # Initialize recognizer class (for recognizing the speech)
    r = sr.Recognizer()

    # Reading Microphone as source
    while True:
        with sr.Microphone() as source:
            print("Talk")
            # listening to speech and storing it in audio_text variable
            r.adjust_for_ambient_noise(source)
            audio_text = r.listen(source,timeout=None,phrase_time_limit=None)
            print("Time over, thanks")

            if(audio_text != ""):
                try:
                    s = r.recognize_google(audio_text,language=code)
                    print("Text: "+s) # prints string of original speech
                    translation = translator.translate(s, src=code[:2], dest=output)    # possible dest are googletrans.LANGCODES, make dropdown

                    print(translation.text)

                    if outputCount == 999:
                        outputCount = 0
                    t = threading.Thread(target=tts, args=(translation.text,output,outputCount,))   #opens thread that will output the translated text
                    t.start()
                    outputCount += 1
                    
                except:
                    print("Sorry, I did not get that")

# speaks translated text
def tts(t, output, outputCount):
    tts = gTTS(text=t, lang=output, slow=False)
    tts.save("good"+ str(outputCount) + ".mp3")
    playsound("good"+ str(outputCount) + ".mp3")
    os.remove("good"+ str(outputCount) + ".mp3")

# starting function called from app.py
def threadedAndBetter2(code, output):
    outputCount = 0
    t1 = threading.Thread(target=inputAri, args=(constants.langs[code], constants.langs2[output], outputCount))
    t1.start()
