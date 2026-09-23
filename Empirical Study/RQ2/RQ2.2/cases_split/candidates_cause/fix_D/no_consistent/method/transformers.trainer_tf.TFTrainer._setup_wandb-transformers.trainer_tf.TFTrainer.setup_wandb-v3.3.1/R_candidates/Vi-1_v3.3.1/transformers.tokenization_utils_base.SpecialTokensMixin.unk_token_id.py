    @property
    def unk_token_id(self) -> Optional[int]:
        """
        :obj:`Optional[int]`: Id of the unknown token in the vocabulary. Returns :obj:`None` if the token has not been
        set.
        """
        if self._unk_token is None:
            return None
        return self.convert_tokens_to_ids(self.unk_token)
