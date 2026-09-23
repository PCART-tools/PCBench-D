    def prepare_inputs_for_generation(self, input_ids, past, **kwargs):
        # only last token for inputs_ids if past is defined in kwargs
        if past is not None:
            input_ids = input_ids[:, -1:]

        inputs_dict = {
            "input_ids": input_ids,
            "past_buckets_states": past,
            "use_cache": kwargs["use_cache"],
        }

        if "num_hashes" in kwargs:
            inputs_dict["num_hashes"] = kwargs["num_hashes"]

        return inputs_dict
