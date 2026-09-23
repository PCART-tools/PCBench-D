    def _convert_id_to_token(self, index: int) -> str:
        """Converts an index (integer) in a token (str) using the vocab."""
        if index in self.encoder:
            return self.encoder[index]
        elif index in self.added_tokens_encoder:
            return self.added_tokens_encoder[index]
        else:
            # assert index > self.offset, f"cannot decode ids between 2 and {self.offset}. Got {index}"
            token = self.sp_model.IdToPiece(index - self.offset)
        return token
