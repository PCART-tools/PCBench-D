    @max_len_sentences_pair.setter
    def max_len_sentences_pair(self, value) -> int:
        # For backward compatibility, allow to try to setup 'max_len_sentences_pair'.
        if value == self.model_max_length - self.num_special_tokens_to_add(pair=True) and self.verbose:
            logger.warning(
                "Setting 'max_len_sentences_pair' is now deprecated. " "This value is automatically set up."
            )
        else:
            raise ValueError(
                "Setting 'max_len_sentences_pair' is now deprecated. " "This value is automatically set up."
            )
