from transformers import RobertaTokenizer
import inspect

def main():
    tokenizer = RobertaTokenizer.from_pretrained('roberta-base')
    tokens = tokenizer.encode("Hello, world!")
    result = tokenizer.add_special_tokens_single_sequence(tokens)
    print("add_special_tokens_single_sequence result:", result)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(tokenizer.add_special_tokens_single_sequence))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()