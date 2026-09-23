    def create_features_from_example(self, tokens_a, tokens_b):
        """Creates examples for a single document."""

        max_num_tokens = self.block_size - self.tokenizer.num_special_tokens_to_add(pair=True)

        tokens_a, tokens_b, _ = self.tokenizer.truncate_sequences(
            tokens_a,
            tokens_b,
            num_tokens_to_remove=len(tokens_a) + len(tokens_b) - max_num_tokens,
            truncation_strategy="longest_first",
        )

        input_id = self.tokenizer.build_inputs_with_special_tokens(tokens_a, tokens_b)
        attention_mask = [1] * len(input_id)
        segment_id = self.tokenizer.create_token_type_ids_from_sequences(tokens_a, tokens_b)
        assert len(input_id) <= self.block_size

        # pad
        while len(input_id) < self.block_size:
            input_id.append(0)
            attention_mask.append(0)
            segment_id.append(0)

        input_id = torch.tensor(input_id)
        attention_mask = torch.tensor(attention_mask)
        segment_id = torch.tensor(segment_id)

        return input_id, attention_mask, segment_id
