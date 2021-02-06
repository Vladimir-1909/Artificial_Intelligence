import pyttsx3 # Проговаривание текста
import speech_recognition as sr
import datetime
import webbrowser

engine = pyttsx3.init()
record = sr.Recognizer()


def sayToMe(talk):
    engine.say(talk)
    engine.runAndWait()


def recognizes_microphone():
    sayToMe("я вас слушаю")
    try:
        with sr.Microphone(device_index=1) as source:
            print("Слушаю...")
            audio = record.listen(source) # В звук от пользователя
        result = (record.recognize_google(audio, language="ru-RU")).lower() # Со свука в текст (ru-RU или en-EN)
        print(result)
        # return sayToMe(f"Вы сказали {result}")

        if result == "скажи время":
            now = datetime.datetime.now()
            str_date = f"Сейчас {str(now.hour)}:{str(now.minute)}"
            print(str_date)
            sayToMe(str_date)
        elif result == "открой веб-сайт":
            webbrowser.open("https://google.com")

    except sr.UnknownValueError:
        return sayToMe("Голос был не распознан")
    except sr.RequestError:
        return sayToMe("Что-то пошло не так!")


recognizes_microphone()