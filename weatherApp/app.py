import requests
import tkinter
import matplotlib.pyplot as plt

api_key = '30d4741c779ba94c470ca1f63045390a'
user_input = input("Enter city: ")
weather_data = requests.get(f"https://api.openweathermap.org/data/2.5/weather?q={user_input}&units=imperial&APPID={api_key}")
if weather_data.json()['cod'] == '404' or weather_data == 'pyt':
    print("No City found")
else:

    #print(weather_data.json())
    weather = weather_data.json()['weather'][0]['main']
    temp  = round((weather_data.json()['main']['temp'] - 32) *5/9)
    print(f'Weather in {user_input} is: {weather} and temperature is: {temp} deg')

x = [1,2,3,4,5,6,7,8,9,10]
y = [0,2,4,6,8,10,12,24,26,28]
plt.plot(x,y)

plt.xlabel('Date')
plt.ylabel('Tempetature')

plt.title(f"Temperature in 7 previous days in {user_input}")

plt.show()