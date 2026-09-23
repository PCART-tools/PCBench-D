from transformers import BertTokenizer
import inspect

def main():
    tokenizer = BertTokenizer.from_pretrained("bert-base-uncased")
    tokens_a = ["hello", "world"]
    tokens_b = ["how", "are", "you"]
    result = tokenizer.add_special_tokens_sequence_pair(tokens_a, tokens_b)
    print("add_special_tokens_sequence_pair result:", result)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(tokenizer.add_special_tokens_sequence_pair))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()