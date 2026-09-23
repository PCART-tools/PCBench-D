    def _concat_inputs_history(self, inputs: List[List[int]], histories: List[Optional[List[int]]], max_length: int):
        """
        Builds an input prepended by the history for this conversation, allowing multi-turn conversation with context
        """
        outputs = []
        for new_input, history in zip(inputs, histories):
            if history is not None:
                new_input = history + new_input
            if len(new_input) > max_length - self.min_length_for_response:
                cutoff_eos_index = 0
                while len(new_input) - cutoff_eos_index > max_length - self.min_length_for_response:
                    if cutoff_eos_index >= len(new_input):
                        break
                    cutoff_eos_index = new_input[cutoff_eos_index:].index(self.tokenizer.eos_token_id)
                    if cutoff_eos_index == 0 or cutoff_eos_index == len(new_input) - 1:
                        break
                    else:
                        new_input = new_input[cutoff_eos_index + 1 :]
            outputs.append(new_input)
        max_len = max([len(item) for item in outputs])
        outputs = [output + [self.pad_token_id] * (max_len - len(output)) for output in outputs]
        outputs = BatchEncoding(
            {"input_ids": outputs, "attention_mask": [[1] * len(outputs)]},
            tensor_type=self.framework,
        )
        return outputs
