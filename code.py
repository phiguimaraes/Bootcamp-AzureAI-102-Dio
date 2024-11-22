# Importing libraries
from bs4 import BeautifulSoup
import requests
import os
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

API_KEY = os.getenv("AZURE_OPENAI_KEY")
ENDPOINT = "https://openiapfdacerto2.openai.azure.com/openai/deployments/gpt-4o-mini/chat/completions?api-version=2024-08-01-preview"

url = "https://dev.to/jasmeet7015/should-you-customize-your-resume-for-every-job-heres-what-i-learned-after-applying-to-100-roles-4bo3"

# Function to extract text from the URL
def extract_text(url):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        for script in soup(["script", "style"]):
            script.decompose()
        return soup.get_text(" ", strip=True)
    else:
        raise ValueError(f"Failed to fetch the URL. Status code: {response.status_code}")

# Function to split text into smaller parts
def split_text(text, chunk_size=900):
    return [text[i:i + chunk_size] for i in range(0, len(text), chunk_size)]

# Function to translate the text
def translate_article(text, lang):
    headers = {
        "Content-Type": "application/json",
        "api-key": API_KEY,
    }

    payload = {
        "messages": [
            {"role": "system", "content": "You act as a text translator."},
            {"role": "user", "content": f"Translate the following text to {lang}:\n{text}"}
        ],
        "temperature": 0.7,
        "top_p": 0.95,
        "max_tokens": 900
    }

    try:
        response = requests.post(ENDPOINT, headers=headers, json=payload)
        response.raise_for_status() 
        return response.json()['choices'][0]['message']['content']
    except requests.RequestException as e:
        print(f"Erro na requisição: {e}")
        return None

# Main function
def main():
    try:
        text = extract_text(url)
        text_parts = split_text(text)
        translated_parts = []
        for part in text_parts:
            translated_part = translate_article(part, "português")
            if translated_part:
                translated_parts.append(translated_part)
        translated_text = "\n".join(translated_parts)
        print("Aqui está a tradução do texto:")
        print(translated_text)
    except Exception as e:
        print(f"Error found: {e}")

if __name__ == "__main__":
    main()
