from transformers import XLMTokenizer
import inspect

def main():
    tokenizer = XLMTokenizer.from_pretrained('xlm-mlm-en-2048')
    tokens_a = tokenizer.tokenize("Hello, how are you?")
    tokens_b = tokenizer.tokenize("I am fine, thank you!")
    result = tokenizer.add_special_tokens_sequence_pair(tokens_a, tokens_b)
    print("add_special_tokens_sequence_pair result:", result)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(XLMTokenizer.add_special_tokens_sequence_pair))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()