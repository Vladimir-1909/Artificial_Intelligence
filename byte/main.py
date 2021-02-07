import speech_recognition as sr
import pyttsx3
import pytesseract
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
from PIL import Image
from pytesseract import image_to_string
from random import randint
import requests
from bs4 import BeautifulSoup
import inspect
import time
import secret
import smtplib
from translate import Translator
import webbrowser


engine = pyttsx3.init()
record = sr.Recognizer()
word = ''
compare = ''


def send_mail(city, temp):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.ehlo()
    server.login('vtgk12ak@gmail.com', secret.secret_key())

    translator = Translator(from_lang="russian", to_lang="english")
    translation = translator.translate(city)
    # print(translation)

    subject = 'Weather mail'
    body = f'Wearheeeer v {translation} {temp}'
    message = f'Subject: {subject}\n{body}'

    server.sendmail(
        'vtgk12ak@gmail.com',
        'v_b_1@bk.ru',
        message
    )
    server.quit()


def sayToMe(talk):
    engine.say(talk)
    engine.runAndWait()


def result():
    try:
        with sr.Microphone(device_index=1) as source:
            print("Слушаю...")
            audio = record.listen(source)
        result = (record.recognize_google(audio, language="ru-RU")).lower()
        print(result)
        return result
    except sr.UnknownValueError:
        sayToMe("Голос был не распознан")
    except sr.RequestError:
        sayToMe("Что-то пошло не так!")


ranNum = randint(1, 4)
hello = {
    1: "здравствуй",
    2: "привет",
    3: "здравствуйте",
    4: "добрый день"
}

sayToMe(hello[ranNum])
sayToMe("Как ваше имя")
name = result()

if name:
    sayToMe("Приятно познакомиться" + name)
sayToMe("Что хотите сделать")

while word != 'пока':

    compare = result()

    if compare == "записать файл":
        text = image_to_string(Image.open('text-ru.jpg'), lang="rus")
        sayToMe("Записываю файл")
        file = open('image_text.txt', 'w')
        file.write(text)
        file.close()

    elif compare == "читать файл":
        if name:
            sayToMe(f"Подождите {name} щас покажу текст")
        else:
            sayToMe(f"Подождите щас покажу текст")
        file = open('image_text.txt', 'rt')
        for t in file:
            print(t)
        file.close()

    elif compare == "погода":
        sayToMe("В каком городе хотите узнать погоду")
        city = result()
        appid = secret.appid()
        url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&units=metric&appid=' + appid
        res = requests.get(url).json()
        temp = int(res["main"]["temp"])
        sayToMe(f"Щас в {city}е {temp}")
        sayToMe("Отправлять погоду на почту")
        send = ""
        while send != "нет":
            send = result()
            if send == "да":
                send = "нет"
                sayToMe("Отправляю погоду на почту")
                send_mail(city, temp)
            elif send == "нет":
                sayToMe("Ну ладно, как хотите")

    elif compare == "открой сайт":
        sayToMe("какой сайт вы хотите открыть")
        sait = result()
        if sait == "ютуб" or sait == "youtube":
            webbrowser.open("https://youtube.com")
        elif sait == "гугл" or sait == "google":
            webbrowser.open("https://google.com")

    elif compare == "доллар в рублях":
        url = 'https://finance.rambler.ru/currencies/'
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36'}

        source = requests.get(url, headers=headers)
        main_text = source.text
        soup = BeautifulSoup(main_text, "html.parser")

        a = soup.find('a', {'class': 'finance-exchange-rate__link'})
        div = (soup.find('div', {'class': 'finance-exchange-rate__value'})).text
        div = inspect.cleandoc(div)[:5]

        doll = f'Курс доллара сейчас: {str(div)}'
        sayToMe(doll)

    elif compare == "как дела":
        sayToMe("Бывало и лучше! у тебя как?")
        mood = result()
        if mood == 'так себе' or mood == 'пойдёт':
            sayToMe(f'Почему у тебя {mood}, ты просто посмотри в окно какая там чудесная погода')
        elif mood == 'отлично' or mood == 'хорошо':
            sayToMe(f'Рад за тебя и за твои {mood}ые дела')

    elif compare == "поспать":
        if name:
            word = "пока"
            sayToMe("Спокойной ночи " + name)
        else:
            word = "пока"
            sayToMe("Спокойной ночи")

    elif compare == "пока":
        word = compare
        if name:
            sayToMe("Пока" + name)
        else:
            sayToMe("Пока пока")