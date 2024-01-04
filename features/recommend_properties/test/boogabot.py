import requests, json
from requests.exceptions import RequestException, JSONDecodeError

url = "https://element-division-image-chip.trycloudflare.com/v1/chat/completions"

headers = {
    "Content-Type": "application/json"
}

history = []

def save_chat_to_file(history, filename="tg.txt"):
    with open(filename, "w") as file:
        json.dump(history, file)

def load_chat_from_file(filename="tg.txt"):
    try:
        with open(filename, "r") as file:
            history = json.load(file)
        return history
    except FileNotFoundError:
        return []

# Load chat history from file if it exists
history = load_chat_from_file()

while True:
    user_input = input("You: ")

    history.append({"role": "user", "content": user_input})
    print()

    ############# payload #############
    data = {
        "mode": "chat",
        "character": "Example",
        "messages": history
    }
    ############# payload #############

    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()

        try:
            response_json = response.json()
            bot_reply = response_json['choices'][0]['message']['content']

            if bot_reply.strip():  # Check if the bot's reply is not blank
                history.append({"role": "oggy", "content": bot_reply})
                print(f"Oggy: {bot_reply}")
                print()

                # Save chat history to file after each interaction
                save_chat_to_file(history)

        except JSONDecodeError:
            print("Error decoding JSON response from the server.")

    except RequestException as e:
        print(f"Error making request: {e}")
