    @property
    def sep_token_id(self) -> Optional[int]:
        """
        :obj:`Optional[int]`: Id of the separation token in the vocabulary, to separate context and query in an input
        sequence. Returns :obj:`None` if the token has not been set.
        """
        if self._sep_token is None:
            return None
        return self.convert_tokens_to_ids(self.sep_token)
