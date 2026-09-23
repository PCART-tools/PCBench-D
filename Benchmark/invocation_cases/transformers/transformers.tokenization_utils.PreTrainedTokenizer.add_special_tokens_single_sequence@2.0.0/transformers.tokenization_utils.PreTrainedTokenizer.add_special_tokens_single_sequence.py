from transformers.tokenization_utils import PreTrainedTokenizer
import inspect

def main():
    # Simulate a tokenizer by subclassing PreTrainedTokenizer
    class MockTokenizer(PreTrainedTokenizer):
        def __init__(self):
            super().__init__()
        
        def _tokenize(self, text):
            return text.split()
        
        def _convert_token_to_id(self, token):
            return ord(token[0]) if token else 0
        
        def _convert_id_to_token(self, index):
            return chr(index)
        
        def convert_tokens_to_string(self, tokens):
            return " ".join(tokens)
    
    tokenizer = MockTokenizer()
    special_tokens = {"cls_token": "[CLS]", "sep_token": "[SEP]"}
    tokenizer.add_special_tokens(special_tokens)
    
    sequence = ["hello", "world"]
    result = tokenizer.add_special_tokens_single_sequence(sequence)
    print("add_special_tokens_single_sequence result:", result)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(PreTrainedTokenizer.add_special_tokens_single_sequence))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()