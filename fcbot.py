import requests
from requests.exceptions import RequestException, JSONDecodeError

url = "https://cc05-121-137-34-45.ngrok-free.app/v1/chat/completions"

headers = {
    "Content-Type": "application/json"
}

history = []

while True:
    user_input = input("You: ")

    history.append({"role": "user", "content": user_input})

    ############# payload #############
    data = {
        "model": "vicuna-13b-v1.5-16k",
        "messages": history
    }
    ############# payload #############

    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        
        try:
            response_json = response.json()
            bot = response_json['choices'][0]['message']['content']
            history.append({"role": "oggy", "content": bot})
            print(f"Oggy: {bot}")
        except JSONDecodeError:
            print("Error decoding JSON response from the server.")

    except RequestException as e:
        print(f"Error making request: {e}")