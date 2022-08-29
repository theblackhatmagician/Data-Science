import speech_recognition as sr
from googletrans import Translator 


def speech2Text(file):
	  
    AUDIO_FILE = file
    
    translator = Translator()
    r = sr.Recognizer()

    with sr.AudioFile(AUDIO_FILE) as source:
        audio = r.record(source)

    try:
        textdata = r.recognize_google(audio)
        textdata = translator.translate(textdata, src='en', dest='ml').text
        print("Text data: " + textdata)
        return textdata

    except sr.UnknownValueError:
        print(" Audio Error")

    except sr.RequestError as e:
        print("Could not request results from Google API; {0}".format(e))


#Write results to a txt file
#file = open("result.txt","w")
#file.write(textdata)
#file.writelines(L) 
#file.close()
