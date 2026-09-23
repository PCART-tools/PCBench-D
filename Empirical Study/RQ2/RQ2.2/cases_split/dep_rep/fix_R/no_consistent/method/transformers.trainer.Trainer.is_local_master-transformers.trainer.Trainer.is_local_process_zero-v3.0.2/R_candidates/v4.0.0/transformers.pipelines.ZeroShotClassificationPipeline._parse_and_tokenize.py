    def _parse_and_tokenize(
        self, sequences, candidate_labels, hypothesis_template, padding=True, add_special_tokens=True, **kwargs
    ):
        """
        Parse arguments and tokenize only_first so that hypothesis (label) is not truncated
        """
        sequence_pairs = self._args_parser(sequences, candidate_labels, hypothesis_template)
        inputs = self.tokenizer(
            sequence_pairs,
            add_special_tokens=add_special_tokens,
            return_tensors=self.framework,
            padding=padding,
            truncation="only_first",
        )

        return inputs
