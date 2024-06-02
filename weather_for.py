from PIL import Image, ImageTk
# Создать оконное приложение. Сделать так, чтобы с помощью API от openweathermap в окне выводилась
# информация о погоде в городе, название которого вводится в поле для ввода. Нужно сделать так,
# чтобы всё было на русском языке. Скомпилировать программу, exe файл вместе с исходным кодом загрузить на Github

from tkinter import *
import requests
from PIL import Image, ImageTk
from tkinter.messagebox import showerror



def save_image(url):
    response = requests.get(url)
    with open("weather_icon.png", "wb") as file:
        file.write(response.content)
    image = Image.open("weather_icon.png")
    return ImageTk.PhotoImage(image)

def show_weather():
    cityname = weather_entry.get()
    if not cityname:
        picture.config(image='')
        weather_info.config(text='')
        showerror('Ошибка', "Строка не может быть пустой ")
    else:
        response = requests.get(
            f"https://api.openweathermap.org/data/2.5/weather?q={cityname}&appid=bdf9b5a5c260533b7b533ef988a0a534&lang=ru")
        if response.status_code != 404:
            response = response.json()
            img = save_image(f"https://openweathermap.org/img/wn/{response["weather"][0]["icon"]}@2x.png")
            picture.config(image=img, background="sky blue")
            picture.image = img
            weather_info.config(text=f"{(response["weather"][0]["description"]).capitalize()}\n"
                                     f"Температура: {round(response["main"]["temp"] - 273.15)} °C\n"
                                     f"Направление ветра: {["Север", "Северо-восток", "Восток", "Юго-восток", "Юг", "Юго-запад", "Запад",
                                                            "Северо-запад"][round( response['wind']['deg']% 360 / 45)]}\n"
                                     f"Скорость ветра: {round(response["wind"]["speed"])} м/c")
        else:
            picture.config(image='')
            weather_info.config(text='')
            showerror('Ошибка', "Указанный город не найден в OpenWeatherMap!")





window = Tk()
window.geometry("600x500")
window.title("Прогноз погоды")
window.resizable(False, False)

welcome_text = Label(window, text="Прогноз погоды", font=("Times New Roman", 40, "bold"))
welcome_text.pack()

weather_entry = Entry(window)
weather_entry.pack()
weather_entry.focus()

btn = Button(window, text="Показать погоду", command=show_weather)
btn.pack(pady=10)

picture = Label(window)
picture.pack()

weather_info = Label(window, font=("Times New Roman", 30))
weather_info.pack()

window.mainloop()
