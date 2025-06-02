import os
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class ChatAPI:
    def __init__(self):
        self.api_key = os.getenv('OPENAI_API_KEY')
        if not self.api_key:
            raise ValueError("Please set your OPENAI_API_KEY in the .env file")
        
        self.api_url = "https://api.openai.com/v1/chat/completions"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        self.conversation_history = []

    def send_message(self, message):
        self.conversation_history.append({"role": "user", "content": message})
        
        data = {
            "model": "gpt-3.5-turbo",
            "messages": self.conversation_history,
            "temperature": 0.7
        }

        try:
            response = requests.post(self.api_url, headers=self.headers, json=data)
            response.raise_for_status()
            assistant_message = response.json()["choices"][0]["message"]["content"]
            self.conversation_history.append({"role": "assistant", "content": assistant_message})
            return assistant_message
        except requests.exceptions.RequestException as e:
            return f"Error: {str(e)}"

def main():
    print("Welcome to the Terminal Chat!")
    print("Type 'quit' to exit the chat")
    print("-" * 50)

    try:
        chat = ChatAPI()
    except ValueError as e:
        print(e)
        return

    while True:
        user_input = input("\nYou: ").strip()
        
        if user_input.lower() == 'quit':
            print("\nGoodbye!")
            break

        if not user_input:
            continue

        response = chat.send_message(user_input)
        print(f"\nAssistant: {response}")

if __name__ == "__main__":
    main() 