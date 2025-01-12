from tkinter import *
import tkinter as tk
from geopy.geocoders import Nominatim
from tkinter import messagebox
from timezonefinder import TimezoneFinder
from datetime import datetime, date
import requests
import pytz
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

root = Tk()
root.title("Weather App")
root.geometry('900x500+300+200')
root.resizable(False, False)

# Load default logo image
logo_image = PhotoImage(file="./icons/default_logo.png")
logo = Label(root, image=logo_image)
logo.place(x=430, y=110)

# Time and Date Labels
date_and_time = tk.Label(root, font=("Helvetica", 20))

# Function to fetch and display weather
def getWeather():
    city = search_bar.get()

    if city == "":
        messagebox.showerror("Input Error", "Please enter a city name")
        return

    geolocator = Nominatim(user_agent="WeatherApp/1.0 (your_email@example.com)")
    try:
        location = geolocator.geocode(city)

    #after succesfuly colecting data search bar is cleared
        search_bar.delete(0, tk.END)
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

        date_and_time.config(text=f"{city}, {current_date}, {current_time}")
        date_and_time.place(x=450, y=450)

        api_key = "30d4741c779ba94c470ca1f63045390a"  # Replace with your OpenWeatherMap API key
        weather_url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
        forecast_url = f"http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={api_key}&units=metric"

        response = requests.get(weather_url)
        forecast_response = requests.get(forecast_url)

        if response.status_code != 200 or forecast_response.status_code != 200:
            messagebox.showerror("API Error", "Unable to fetch data")
            return

        data = response.json()
        forecast_data = forecast_response.json()

        temp = data["main"]["temp"]
        humidity = data["main"]["humidity"]
        pressure = data["main"]["pressure"]
        wind = data["wind"]["speed"]
        description = data["weather"][0]["description"]

        # Rain and snow data
        rain = data.get("rain", {}).get("1h", "ND")
        snow = data.get("snow", {}).get("1h", "ND")

        t.config(text=f"{temp}°C")
        w.config(text=f"{wind} m/s")
        p.config(text=f"{pressure} hPa")
        d.config(text=f"{description.capitalize()}")
        h.config(text=f"{humidity}%")
        r.config(text=f"{rain} mm")
        s.config(text=f"{snow} mm")

        # Change logo based on weather description
        if 'clear' in description:
            new_logo = PhotoImage(file="./icons/sunny.png")
        elif 'cloud' in description:
            new_logo = PhotoImage(file="icons/cloudy.png")
        elif 'rain' in description:
            new_logo = PhotoImage(file="./icons/rainy.png")
        elif 'snow' in description:
            new_logo = PhotoImage(file="./icons/snowy.png")
        else:
            new_logo = PhotoImage(file="./icons/default_logo.png")  # Default logo for unknown conditions

        logo.config(image=new_logo)
        logo.image = new_logo  # Keep reference

        # Save forecast data for graph
        global forecast_times, forecast_temps
        forecast_times = [item["dt_txt"] for item in forecast_data["list"][:8]]
        forecast_temps = [item["main"]["temp"] for item in forecast_data["list"][:8]]

    except requests.exceptions.RequestException as e:
        messagebox.showerror("Error", f"Network Error: {e}")
    except Exception as e:
        messagebox.showerror("Error", f"An unexpected error occurred: {e}")

# Function to display the graph in a new window
# Function to display the graph in a new window
def getGraph():
    if not forecast_times or not forecast_temps:
        messagebox.showerror("Error", "No forecast data available. Please search for a city first.")
        return

    # Format the times to "HH:MM AM/PM"
    try:
        formatted_times = [
            datetime.strptime(time, "%Y-%m-%d %H:%M:%S").strftime("%I:%M %p")
            for time in forecast_times
        ]
    except Exception as e:
        messagebox.showerror("Error", f"Failed to format times: {e}")
        return

    # Open a new window for the graph
    graph_window = Toplevel(root)
    graph_window.title("Weather Forecast Graph")
    graph_window.geometry("1000x700")  # Adjusted size for the window

    # Create the matplotlib figure
    fig, ax = plt.subplots(figsize=(12, 6), dpi=100)  # Increased figure size
    ax.bar(formatted_times, forecast_temps, color="skyblue")
    ax.set_title("Temperature Forecast", fontsize=16)
    ax.set_xlabel("Time", fontsize=14)
    ax.set_ylabel("Temperature (°C)", fontsize=14)

    # Rotate x-axis labels for readability
    ax.set_xticks(range(len(formatted_times)))
    ax.set_xticklabels(formatted_times, rotation=45, ha="right", fontsize=10)

    # Adjust layout for better spacing
    fig.tight_layout()

    # Embed the matplotlib figure in Tkinter
    canvas = FigureCanvasTkAgg(fig, master=graph_window)
    canvas.draw()
    canvas.get_tk_widget().pack()


# Search Bar and Button
search_bar = Entry(root, font=("Helvetica", 20))
search_bar.place(x=450, y=10)
search_bar.focus()

search_bar.bind("<Return>", lambda event=None: getWeather())  # Bind Enter key

search_icon_button = Button(text="Search", borderwidth=0, cursor="hand2", width=8, height=1, command=getWeather)
search_icon_button.place(x=685, y=17)

# Left Output Box
bottom_box = tk.Label(root, width=35, height=600, background="lightblue")
bottom_box.place(x=0, y=1)

# Labels on the left
wind_label = tk.Label(root, text="WIND", font=("Helvetica", 20, "bold"), fg="white", bg="lightblue")
wind_label.place(x=30, y=15)

press_label = tk.Label(root, text="PRESSURE", font=("Helvetica", 20, "bold"), fg="white", bg="lightblue")
press_label.place(x=30, y=85)

desc_label = tk.Label(root, text="DESCRIPTION", font=("Helvetica", 20, "bold"), fg="white", bg="lightblue")
desc_label.place(x=30, y=155)

hum_label = tk.Label(root, text="HUMIDITY", font=("Helvetica", 20, "bold"), fg="white", bg="lightblue")
hum_label.place(x=30, y=225)

rain_label = tk.Label(root, text="RAIN", font=("Helvetica", 20, "bold"), fg="white", bg="lightblue")
rain_label.place(x=30, y=295)

snow_label = tk.Label(root, text="SNOW", font=("Helvetica", 20, "bold"), fg="white", bg="lightblue")
snow_label.place(x=30, y=365)

# Labels for Output
t = tk.Label(root, text="...", font=("Arial", 22), bg="white")
t.place(x=600, y=50)

w = tk.Label(root, text="...", font=("Arial", 20), bg="lightblue")
w.place(x=30, y=50)

p = tk.Label(root, text="...", font=("Arial", 20), bg="lightblue")
p.place(x=30, y=120)

d = tk.Label(root, text="...", font=("Arial", 20), bg="lightblue")
d.place(x=30, y=190)

h = tk.Label(root, text="...", font=("Arial", 20), bg="lightblue")
h.place(x=30, y=260)

r = tk.Label(root, text="...", font=("Arial", 20), bg="lightblue")
r.place(x=30, y=330)

s = tk.Label(root, text="...", font=("Arial", 20), bg="lightblue")
s.place(x=30, y=400)

# Graph Button
graph_button = Button(root, text="Future Weather", font=("Arial", 20), bg="grey", fg="white", command=getGraph)
graph_button.place(x=22, y=430)

# Global variables for forecast data
forecast_times = []
forecast_temps = []

root.mainloop()
