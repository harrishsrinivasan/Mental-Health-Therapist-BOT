# 👨‍⚕️ Therapist BOT - Mental Health Therapist Chatbot 

This project runs a streamlit web-based chatbot that provides empathetic mental health support.
It uses llama3.1:8b as its local LLM model using Ollama and when online it uses gemini2.5 flash using google api.
It uses **two separate containers**:

1. **Ollama** – Offline AI model backend  
2. **Streamlit** – Frontend chatbot interface  

Docker makes it easy to run everything without installing dependencies locally.

---

## Features

- Compassionate mental health support for sensitive topics.
- Online mode via Google Gemini API or offline mode via Ollama in the same chat.


---

## Requirements

- docker
- `.env` file with your Google API key

---

## Setup Instructions

### 1. Clone the repository

```bash
git clone https://github.com/<your-username>/mental-health-therapist.git
cd mental-health-therapist
```

### 2. Create a .env file

```bash
GOOGLE_API_KEY=<YOUR_GOOGLE_API_KEY>
```

### 3. Create a virtual environment (optional)
```
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

### 4. Install dependencies
```bash
pip install -r requirements.txt
```

### 5. Install Docker
then run this command in terminal
```bash
docker-compose up --build -d
```
### 6. Run Ollama in docker 
```bash
docker exec -it ollama ollama pull llama3.1:8b
```

Your Streamlit app will start to work now

### 7. Deactivate container
after using the app you can deactivate the container using the command

```
docker-compose down
```
