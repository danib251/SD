from weatherData import WeatherData

if __name__ == '__main__':
    weather_data = WeatherData()

    # Generar 5 registros de datos de tiempo
    for i in range(5):
        data = weather_data.generate_data()
        print(f"Registro {i+1}: Temperatura {data}")