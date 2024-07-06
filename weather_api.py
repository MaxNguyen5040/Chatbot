import requests

def get_weather(location):
    api_key = "YOUR_WEATHER_API_KEY"
    base_url = f"http://api.openweathermap.org/data/2.5/weather?q={location}&appid={api_key}"
    response = requests.get(base_url)
    if response.status_code == 200:
        data = response.json()
        weather = data['weather'][0]['description']
        temperature = data['main']['temp']
        return f"The weather in {location} is {weather} with a temperature of {temperature - 273.15:.2f}°C."
    else:
        return "Sorry, I couldn't fetch the weather information."

# Modify the handle_intent function to handle weather queries

def handle_intent(intent, entities):
    try:
        if intent == 'weather_query':
            location = next((entity['value'] for entity in entities if entity['entity'] == 'location'), None)
            if not location:
                raise ValueError("Location not provided")
            return get_weather(location)
        elif intent == 'flight_booking':
            destination = next((entity['value'] for entity in entities if entity['entity'] == 'location'), None)
            date = next((entity['value'] for entity in entities if entity['entity'] == 'date'), None)
            if not destination or not date:
                raise ValueError("Destination or date not provided")
            return f"Booking a flight to {destination} on {date}."
        else:
            return "I'm not sure how to help with that."
    except Exception as e:
        return str(e)

# Example usage
user_message = "What's the weather like in New York?"
intent, entities = recognize_intent(user_message)
response = handle_intent(intent, entities)
print(response)
