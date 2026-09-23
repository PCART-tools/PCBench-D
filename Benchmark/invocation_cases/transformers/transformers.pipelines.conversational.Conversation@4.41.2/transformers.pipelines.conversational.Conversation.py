from transformers import Conversation
import inspect

def main():
    # Create a conversation instance with initial input
    conversation = Conversation("Hello, how are you?")
    print("Conversation instance:", conversation)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(Conversation))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()