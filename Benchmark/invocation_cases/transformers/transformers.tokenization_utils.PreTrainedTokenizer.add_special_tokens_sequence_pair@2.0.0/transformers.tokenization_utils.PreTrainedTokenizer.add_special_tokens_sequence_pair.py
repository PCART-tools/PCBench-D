import inspect
from transformers import PreTrainedTokenizer

class MockTokenizer(PreTrainedTokenizer):
    def __init__(self, **kwargs):
        super().__init__(unk_token='[UNK]', **kwargs)
        self.vocab = {'[UNK]': 0}
        self.ids_to_tokens = {0: '[UNK]'}
        self.special_tokens_map_extended = {}

    def _convert_token_to_id(self, token):
        if token not in self.vocab:
            idx = len(self.vocab)
            self.vocab[token] = idx
            self.ids_to_tokens[idx] = token
        return self.vocab[token]


def main():
    tokenizer = MockTokenizer()
    tokenizer.add_special_tokens({'sep_token': '[SEP]', 'cls_token': '[CLS]'})

    token_ids_0 = [101, 200, 300]
    token_ids_1 = [400, 500, 600]
    result = tokenizer.add_special_tokens_sequence_pair(token_ids_0, token_ids_1)
    print("add_special_tokens_sequence_pair result:", result)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(tokenizer.add_special_tokens_sequence_pair))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()
