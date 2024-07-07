def get_local_news(location):
    # Mock function to return local news
    news = {
        "New York": "Today's top news in New York...",
        "San Francisco": "Today's top news in San Francisco...",
    }
    return news.get(location, "No news available for this location.")

def get_local_weather(location):
    # Mock function to return local weather
    weather = {
        "New York": "The weather in New York is sunny.",
        "San Francisco": "The weather in San Francisco is foggy.",
    }
    return weather.get(location, "Weather data not available for this location.")