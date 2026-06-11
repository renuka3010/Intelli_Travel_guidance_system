# IntelliTravel: AI-Powered Travel Guidance System

## Overview

IntelliTravel is an AI-powered travel assistant designed to help travelers access destination information, travel guides, weather updates, currency exchange rates, and travel-related insights through an interactive chatbot interface.

The system leverages Generative AI, PDF-based knowledge retrieval, and real-time API integrations to provide accurate and personalized travel guidance.

---

## Features

* AI-powered travel chatbot
* Destination information and travel guidance
* PDF-based travel guide knowledge retrieval
* Real-time weather updates
* Live currency exchange rates
* Travel news integration
* Secure API key management using environment variables
* User-friendly interface
* Travel recommendations and assistance

---

## Technologies Used

### Programming Language

* Python

### Libraries & Frameworks

* Streamlit
* PyPDF2
* Requests
* Python-dotenv

### APIs

* Groq API (LLM Integration)
* OpenWeather API
* ExchangeRate API
* GNews API

### Version Control

* Git
* GitHub

---

## Project Structure

```text
IntelliTravel/
│
├── data/
│   ├── travel_guides/
│   └── static/
│
├── pages/
│   └── train_schedule.py
│
├── main.py
├── llm_helper.py
├── post_generator.py
├── security_enhancements.py
├── travel_guide_helper.py
│
├── .env
├── .gitignore
├── README.md
└── requirements.txt
```

---

## Installation

### Clone Repository

```bash
git clone https://github.com/your-username/Intelli_Travel_guidance_system.git
cd Intelli_Travel_guidance_system
```

### Create Virtual Environment

```bash
python -m venv venv
```

Activate Environment:

Windows:

```bash
venv\Scripts\activate
```

Linux/Mac:

```bash
source venv/bin/activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Environment Variables

Create a `.env` file in the project root directory:

```env
GROQ_API_KEY=your_groq_api_key
WEATHER_API_KEY=your_weather_api_key
EXCHANGE_RATE_API_KEY=your_exchange_rate_api_key
GNEWS_API_KEY=your_gnews_api_key
```

⚠️ Never upload your `.env` file to GitHub.

---

## Running the Application

```bash
streamlit run main.py
```

The application will be available locally in your browser.

---

## Use Cases

* Travel planning
* Destination exploration
* Weather checking
* Currency conversion assistance
* Travel information retrieval
* AI-powered tourist guidance

---

## Future Enhancements

* Hotel recommendation system
* Flight information integration
* Multi-language support
* Voice-enabled chatbot
* Personalized travel itineraries
* Maps and navigation integration

---

## Author

Renuka Mahajan

Software Developer | AI Enthusiast | Generative AI Researcher

---

## License

This project is developed for educational and research purposes.
