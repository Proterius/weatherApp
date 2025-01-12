from tkinter import *
import tkinter as tk
from geopy.geocoders import Nominatim
from tkinter import messagebox
from timezonefinder import TimezoneFinder
from datetime import datetime
from datetime import date
import requests
import pytz

root = Tk()
root.title("Weather App")
root.geometry('900x500+300+200')
root.resizable(False, False)

# Load default logo image
logo_image = PhotoImage(file="./icons/default_logo.png")
logo = Label(root, image=logo_image)
logo.place(x=430, y=110)

# Time and Date Labels
date_and_time = date.today()
date_and_time = tk.Label(root, font = ("Helvetica", 20))


def getWeather():
    city = search_bar.get()

    if city == "":
        messagebox.showerror("Input Error", "Please enter a city name")
        return

    geolocator = Nominatim(user_agent="WeatherApp/1.0 (your_email@example.com)")
    try:
        location = geolocator.geocode(city)

        if location is None:
            messagebox.showerror("Error", f"Could not find the location: {city}")
            return

        obj = TimezoneFinder()
        result = obj.timezone_at(lng=location.longitude, lat=location.latitude)

        if result is None:
            messagebox.showerror("Error", "Could not determine the timezone")
            return

        home = pytz.timezone(result)
        local_time = datetime.now(home)
        current_time = local_time.strftime("%I:%M %p")  # 12-hour format (AM/PM)
        current_date = local_time.strftime("%A, %d %B %Y")

        date_and_time.config(text = f"{current_date}, {current_time}")
        date_and_time.place(x = 450, y = 450)

        api_key = "30d4741c779ba94c470ca1f63045390a"  # Replace with your OpenWeatherMap API key
        weather_url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"

        response = requests.get(weather_url)

        if response.status_code != 200:
            messagebox.showerror("API Error", f"Error {response.status_code}: Unable to fetch data")
            return

        data = response.json()

        temp = data["main"]["temp"]
        humidity = data["main"]["humidity"]
        pressure = data["main"]["pressure"]
        wind = data["wind"]["speed"]
        description = data["weather"][0]["description"]

        t.config(text=f"{temp}°C")
        w.config(text=f"{wind} m/s")
        p.config(text=f"{pressure} hPa")
        d.config(text=f"{description.capitalize()}")
        h.config(text=f"{humidity}%")

        # Change logo based on weather description
        if 'clear' in description:
            logo_image = PhotoImage(file="./icons/sunny.png")
        elif 'cloud' in description:
            logo_image = PhotoImage(file="icons/cloudy.png")
        elif 'rain' in description:
            logo_image = PhotoImage(file="./icons/rainy.png")
        elif 'snow' in description:
            logo_image = PhotoImage(file="./icons/snowy.png")
        else:
            logo_image = PhotoImage(file="./icons/default_logo.png")  # Default logo for unknown conditions

        # Update the logo image
        logo.config(image=logo_image)
        logo.image = logo_image  # Keep a reference to prevent garbage collection

    except requests.exceptions.RequestException as e:
        messagebox.showerror("Error", f"Network Error: {e}")
    except Exception as e:
        messagebox.showerror("Error", f"An unexpected error occurred: {e}")




#Search Bar and Button
search_bar = Entry(root, font=("Helvetica", 20), text='Search...')
search_bar.place(x=450, y=10)
search_bar.focus()

# Binding the Enter key to the getWeather function
search_bar.bind("<Return>", lambda event=None: getWeather())

search_icon_button = Button(text='Search', borderwidth=0, cursor="hand2", width=8, height=1, command=getWeather)
search_icon_button.place(x=685, y=17)

# Left Output Box
bottom_box = tk.Label(root, width=35, height=600, background="lightblue")
bottom_box.place(x = 0, y = 1)

# Labels on the left
wind_label = tk.Label(root, text="WIND", font=("Helvetica", 20, 'bold'), fg="white", bg='lightblue')
wind_label.place(x=30, y=15)

press_label = tk.Label(root, text="PRESSURE", font=("Helvetica", 20, 'bold'), fg="white", bg='lightblue')
press_label.place(x=30, y=85)

desc_label = tk.Label(root, text="DESCRIPTION", font=("Helvetica", 20, 'bold'), fg="white", bg='lightblue')
desc_label.place(x=30, y=155)

hum_label = tk.Label(root, text="HUMIDITY", font=("Helvetica", 20, 'bold'), fg="white", bg='lightblue')
hum_label.place(x=30, y=225)

# Labels for Output
t = tk.Label(root, text='123', font=('Arial', 22), bg='white')
t.place(x=600, y=50)

w = tk.Label(root, text='123', font=("Arial", 20), bg='lightblue')
w.place(x=30, y=50)

p = tk.Label(root, text='123', font=("Arial", 20), bg='lightblue')
p.place(x=30, y=120)

d = tk.Label(root, text='123', font=("Arial", 20), bg='lightblue')
d.place(x=30, y=190)

h = tk.Label(root, text='123', font=("Arial", 20), bg='lightblue')
h.place(x=30, y=260)

graph = Button(root, text = 'Future weather', font = ("Ariel", 20) , background = "grey", border = 0, width = 13, command = getGraph )
graph.place(x = 22, y = 430)

def getGraph():


root.mainloop()
