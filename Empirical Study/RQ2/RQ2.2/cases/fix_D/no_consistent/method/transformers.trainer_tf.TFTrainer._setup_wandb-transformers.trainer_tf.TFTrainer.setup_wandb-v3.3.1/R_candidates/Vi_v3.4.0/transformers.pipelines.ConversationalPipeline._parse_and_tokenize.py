    def _parse_and_tokenize(self, *args, **kwargs):
        """
        Parse arguments and tokenize, adding an EOS token at the end of the user input
        """
        # Parse arguments
        inputs = self._args_parser(*args, **kwargs)
        inputs = self.tokenizer.batch_encode_plus(inputs, add_special_tokens=False, padding=False).get("input_ids", [])
        for input in inputs:
            input.append(self.tokenizer.eos_token_id)
        return inputs
