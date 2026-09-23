    def _parse_and_tokenize(self, *args, padding=True, add_special_tokens=True, **kwargs):
        """
        Parse arguments and tokenize only_first so that hypothesis (label) is not truncated
        """
        inputs = self._args_parser(*args, **kwargs)
        inputs = self.tokenizer(
            inputs,
            add_special_tokens=add_special_tokens,
            return_tensors=self.framework,
            padding=padding,
            truncation="only_first",
        )

        return inputs
