    def prepare_inputs_for_generation(self, input_ids, past, **kwargs):
        # Add dummy token at the end (no attention on this one)

        effective_batch_size = input_ids.shape[0]
        dummy_token = torch.zeros((effective_batch_size, 1), dtype=torch.long, device=input_ids.device)

        # At every pass, the attention values for the new token and the two last generated tokens
        # are computed, the rest is reloaded from the `past` cache. A purely auto-regressive model would have
        # offset = 1; offset = 2 seems to have slightly better computation.
        offset = 2

        if past:
            input_ids = torch.cat([input_ids[:, -offset:], dummy_token], dim=1)
        else:
            input_ids = torch.cat([input_ids, dummy_token], dim=1)

        # Build permutation mask so that previous tokens don't see last token
        sequence_length = input_ids.shape[1]
        perm_mask = torch.zeros(
            (effective_batch_size, sequence_length, sequence_length), dtype=torch.float, device=input_ids.device
        )
        perm_mask[:, :, -1] = 1.0

        # We'll only predict the last token
        target_mapping = torch.zeros(
            (effective_batch_size, 1, sequence_length), dtype=torch.float, device=input_ids.device
        )
        target_mapping[:, 0, -1] = 1.0

        inputs = {
            "input_ids": input_ids,
            "perm_mask": perm_mask,
            "target_mapping": target_mapping,
            "use_cache": kwargs["use_cache"],
        }

        # if past is defined in model kwargs then use it for faster decoding
        if past:
            inputs["mems"] = tuple(layer_past[:-offset, :, :] for layer_past in past)

        return inputs
