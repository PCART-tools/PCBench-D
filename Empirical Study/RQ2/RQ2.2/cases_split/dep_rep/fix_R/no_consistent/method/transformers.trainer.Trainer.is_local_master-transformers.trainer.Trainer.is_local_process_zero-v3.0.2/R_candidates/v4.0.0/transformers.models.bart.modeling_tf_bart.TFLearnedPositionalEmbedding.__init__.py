    def __init__(self, num_embeddings: int, embedding_dim: int, padding_idx: int, offset, **kwargs):
        # Bart is set up so that if padding_idx is specified then offset the embedding ids by 2
        # and adjust num_embeddings appropriately. Other models dont have this hack
        self.offset = offset
        assert padding_idx is not None, "padding_idx cannot be None"
        num_embeddings += offset
        super().__init__(num_embeddings, embedding_dim, **kwargs)
