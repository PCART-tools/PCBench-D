    def prepare_inputs_for_generation(self, input_ids, past, attention_mask, use_cache, encoder_outputs, **kwargs):
        return {
            "decoder_input_ids": input_ids,
            "past_key_values": past,
            "encoder_outputs": encoder_outputs,
            "attention_mask": attention_mask,
            "use_cache": use_cache,
        }
