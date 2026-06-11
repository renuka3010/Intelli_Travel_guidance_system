import os
import requests
import PyPDF2
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


def load_all_pdfs(directory_path):
    """Combine text from all PDFs in a directory."""
    combined_text = ""

    if not os.path.exists(directory_path):
        return "PDF directory not found."

    for filename in os.listdir(directory_path):
        if filename.lower().endswith(".pdf"):
            pdf_path = os.path.join(directory_path, filename)

            try:
                with open(pdf_path, "rb") as file:
                    reader = PyPDF2.PdfReader(file)

                    for page in reader.pages:
                        text = page.extract_text()
                        if text:
                            combined_text += text + "\n"

            except Exception as e:
                print(f"Error reading {filename}: {e}")

    return combined_text


def get_weather(city):
    """Fetch real-time weather for a given city."""
    api_key = os.getenv("WEATHER_API_KEY")

    if not api_key:
        return {"error": "WEATHER_API_KEY not found in .env"}

    url = (
        f"https://api.openweathermap.org/data/2.5/weather"
        f"?q={city}&appid={api_key}&units=metric"
    )

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()

        data = response.json()

        return {
            "temperature": data["main"]["temp"],
            "weather": data["weather"][0]["description"],
            "city": data["name"]
        }

    except requests.exceptions.RequestException as e:
        return {"error": str(e)}


def get_currency_rate(from_currency, to_currency):
    """Fetch real-time currency exchange rate."""
    api_key = os.getenv("EXCHANGE_RATE_API_KEY")

    if not api_key:
        return {"error": "EXCHANGE_RATE_API_KEY not found in .env"}

    url = (
        f"https://v6.exchangerate-api.com/v6/"
        f"{api_key}/pair/{from_currency}/{to_currency}"
    )

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()

        data = response.json()

        return {
            "from": from_currency.upper(),
            "to": to_currency.upper(),
            "rate": data.get("conversion_rate")
        }

    except requests.exceptions.RequestException as e:
        return {"error": str(e)}


def get_travel_news():
    """Fetch latest travel news."""
    api_key = os.getenv("GNEWS_API_KEY")

    if not api_key:
        return {"error": "GNEWS_API_KEY not found in .env"}

    url = (
        f"https://gnews.io/api/v4/search"
        f"?q=travel&lang=en&token={api_key}"
    )

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()

        data = response.json()

        news_list = []

        for article in data.get("articles", [])[:5]:
            news_list.append({
                "title": article.get("title"),
                "description": article.get("description"),
                "url": article.get("url")
            })

        return news_list

    except requests.exceptions.RequestException as e:
        return {"error": str(e)}


if __name__ == "__main__":
    print(get_weather("Mumbai"))
    print(get_currency_rate("USD", "INR"))
    print(get_travel_news())