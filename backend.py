# import requests package/ module
import requests

# API Key
API_KEY = "d86b5e982f06996fa1503e0c8f4622e6"

# function used in GUI to return weather data from https://openweathermap.org api
def get_data(location, forecast_days=None):
    url = f"https://api.openweathermap.org/data/2.5/forecast?q={location}&appid={API_KEY}"
    response = requests.get(url)
    data = response.json()
    filtered_data = data['list']
    number_values = 8 * forecast_days
    filtered_data = filtered_data[:number_values]
    return filtered_data


if __name__ == "__main__":
    print(get_data(location="Knoxville", forecast_days=3))