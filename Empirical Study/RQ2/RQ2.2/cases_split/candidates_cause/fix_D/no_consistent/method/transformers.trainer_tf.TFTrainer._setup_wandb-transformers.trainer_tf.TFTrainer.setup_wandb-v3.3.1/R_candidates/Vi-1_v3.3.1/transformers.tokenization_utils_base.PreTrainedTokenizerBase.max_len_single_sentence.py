    @max_len_single_sentence.setter
    def max_len_single_sentence(self, value) -> int:
        # For backward compatibility, allow to try to setup 'max_len_single_sentence'.
        if value == self.model_max_length - self.num_special_tokens_to_add(pair=False) and self.verbose:
            logger.warning(
                "Setting 'max_len_single_sentence' is now deprecated. " "This value is automatically set up."
            )
        else:
            raise ValueError(
                "Setting 'max_len_single_sentence' is now deprecated. " "This value is automatically set up."
            )
