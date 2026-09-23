    def __call__(self, examples: List[Dict[str, torch.Tensor]]) -> Dict[str, torch.Tensor]:
        """
        The input should contain negative examples, :class:`~transformers.DataCollatorForNextSentencePrediction` will not generate any negative examples.
        Args:
            examples (:obj:`List[Dict]`): Each dictionary should have the following keys:
                  - ``tokens_a``: A sequence of tokens, which should appear before ``tokens_b`` in the text.
                  - ``tokens_b``: A sequence of tokens, which should appear after ``tokens_a`` in the text.
                  - ``is_random_next``: 1 if this pair is generated randomly, else 0.
        """

        tokens_a = [e["tokens_a"] for e in examples]
        tokens_b = [e["tokens_b"] for e in examples]
        nsp_labels = [1 if e["is_random_next"] else 0 for e in examples]

        input_ids = []
        segment_ids = []
        attention_masks = []

        assert len(tokens_a) == len(tokens_b)
        for i in range(len(tokens_a)):
            input_id, attention_mask, segment_id = self.create_features_from_example(tokens_a[i], tokens_b[i])
            input_ids.append(input_id)
            segment_ids.append(segment_id)
            attention_masks.append(attention_mask)
        if self.mlm:
            input_ids, mlm_labels = self.mask_tokens(self._tensorize_batch(input_ids))
        else:
            input_ids = self._tensorize_batch(input_ids)

        result = {
            "input_ids": input_ids,
            "attention_mask": self._tensorize_batch(attention_masks),
            "token_type_ids": self._tensorize_batch(segment_ids),
            "masked_lm_labels": mlm_labels if self.mlm else None,
            "next_sentence_label": torch.tensor(nsp_labels),
        }
        if self.mlm:
            result["masked_lm_labels"] = mlm_labels
        return result
