from transformers import XLMTokenizer
import inspect

def main():
    # Initialize the tokenizer
    tokenizer = XLMTokenizer.from_pretrained("xlm-mlm-en-2048")
    
    # Test data
    input_ids = tokenizer.encode("Hello, how are you?")
    
    # Call the target API
    result = tokenizer.add_special_tokens_single_sequence(input_ids)
    print("add_special_tokens_single_sequence result:", result)
    
    print("-----getsource_output-----")
    try:
        print(inspect.getsource(XLMTokenizer.add_special_tokens_single_sequence))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()