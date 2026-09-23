    def _convert_token_to_id(self, token):
        """ Converts a token (str) in an id using the vocab. """
        if token in self.fairseq_tokens_to_ids:
            return self.fairseq_tokens_to_ids[token]
        elif self.sp_model.PieceToId(token) == 0:
            # Convert sentence piece unk token to fairseq unk token index
            return self.unk_token_id
        return self.fairseq_offset + self.sp_model.PieceToId(token)
