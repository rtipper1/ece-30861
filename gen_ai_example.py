import requests
import os

api_key = os.environ.get("API_KEY")
if not api_key:
    raise Exception("API key not set")

url = "https://genai.rcac.purdue.edu/api/chat/completions"
headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json"
}
body = {
    "model": "llama3.1:latest",
    "messages": [
        {
            "role": "user",
            "content": "give me a float between 0 and 1. Only return the number, no additional text"
        }
    ],
    # Removed the 'stream': True parameter to avoid chunked encoding issues
}

try:
    response = requests.post(url, headers=headers, json=body)
    response.raise_for_status()
    response_data = response.json()
    
    output = response_data["choices"][0]["message"]["content"]
    print(response_data)
    print(type(float(output)))
    print(output)
except (ValueError, KeyError) as e:
    print(f"Error extracting output: {e}")