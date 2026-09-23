    def prepare_inputs_for_generation(self, inputs, past, **model_kwargs):
        inputs = {"inputs": inputs}

        # if past is defined in model kwargs then use it for faster decoding
        if past:
            inputs["mems"] = past

        return inputs
