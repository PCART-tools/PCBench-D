    @property
    def mask_token_id(self) -> Optional[int]:
        """
        :obj:`Optional[int]`: Id of the mask token in the vocabulary, used when training a model with masked-language
        modeling. Returns :obj:`None` if the token has not been set.
        """
        if self._mask_token is None:
            return None
        return self.convert_tokens_to_ids(self.mask_token)
