    @property
    def additional_special_tokens_ids(self) -> List[int]:
        """
        :obj:`List[int]`: Ids of all the additional special tokens in the vocabulary.
        Log an error if used while not having been set.
        """
        return self.convert_tokens_to_ids(self.additional_special_tokens)
