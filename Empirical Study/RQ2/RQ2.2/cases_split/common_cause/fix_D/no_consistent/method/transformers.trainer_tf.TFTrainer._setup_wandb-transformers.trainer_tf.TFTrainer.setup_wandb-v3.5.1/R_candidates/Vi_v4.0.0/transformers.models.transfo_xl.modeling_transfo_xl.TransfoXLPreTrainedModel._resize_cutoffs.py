    def _resize_cutoffs(self, new_num_tokens, new_emb_size, new_embedding_shapes, layer):
        embeddings = self.get_input_embeddings()

        for i in range(layer, len(embeddings.cutoffs)):
            embeddings.cutoffs[i] = sum(new_embedding_shapes[: i + 1])

        embeddings.cutoff_ends = [0] + embeddings.cutoffs
        embeddings.n_token = new_num_tokens

        self.config.cutoffs = embeddings.cutoffs[:-1]

        return embeddings.cutoffs
