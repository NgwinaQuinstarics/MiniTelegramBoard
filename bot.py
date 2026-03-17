# bot.py
def respond(message):
    if "hi" in message.lower():
        return "Hello! Nice to meet you."
    elif "bye" in message.lower():
        return "Goodbye!"
    else:
        return "I don't understand that yet."

print("Welcome to your mini chat board! Type 'quit' to exit.")

while True:
    user_input = input("You: ")
    if user_input.lower() == "quit":
        print("Exiting... Bye!")
        break
    reply = respond(user_input)
    print("Bot:", reply)