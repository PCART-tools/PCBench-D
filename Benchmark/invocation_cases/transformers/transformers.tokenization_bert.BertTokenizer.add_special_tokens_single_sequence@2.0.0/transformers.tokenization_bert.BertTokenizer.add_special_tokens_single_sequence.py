from transformers import BertTokenizer
import inspect

def main():
    tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
    sequence = tokenizer.encode("Hello, how are you?")
    result = tokenizer.add_special_tokens_single_sequence(sequence)
    print("add_special_tokens_single_sequence result:", result)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(tokenizer.add_special_tokens_single_sequence))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()