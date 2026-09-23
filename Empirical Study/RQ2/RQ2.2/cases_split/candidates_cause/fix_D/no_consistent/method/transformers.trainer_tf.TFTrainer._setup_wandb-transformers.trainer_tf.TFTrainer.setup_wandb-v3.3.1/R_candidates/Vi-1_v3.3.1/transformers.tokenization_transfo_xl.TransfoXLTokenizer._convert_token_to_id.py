    def _convert_token_to_id(self, sym):
        """ Converts a token (str) in an id using the vocab. """
        if sym in self.sym2idx:
            return self.sym2idx[sym]
        else:
            # logger.info('encounter unk {}'.format(sym))
            # assert '<eos>' not in sym
            if hasattr(self, "unk_idx"):
                return self.sym2idx.get(sym, self.unk_idx)
            # Backward compatibility with pre-trained models
            elif "<unk>" in self.sym2idx:
                return self.sym2idx["<unk>"]
            elif "<UNK>" in self.sym2idx:
                return self.sym2idx["<UNK>"]
            else:
                raise ValueError("Token not in vocabulary and no <unk> token in vocabulary for replacement")
