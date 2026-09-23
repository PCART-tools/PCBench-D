    @nn.compact
    def __call__(self, input_ids, token_type_ids, position_ids, attention_mask):

        # Embed
        w_emb = FlaxBertEmbedding(self.vocab_size, self.hidden_size, name="word_embeddings")(
            jnp.atleast_2d(input_ids.astype("i4"))
        )
        p_emb = FlaxBertEmbedding(self.max_length, self.hidden_size, name="position_embeddings")(
            jnp.atleast_2d(position_ids.astype("i4"))
        )
        t_emb = FlaxBertEmbedding(self.type_vocab_size, self.hidden_size, name="token_type_embeddings")(
            jnp.atleast_2d(token_type_ids.astype("i4"))
        )

        # Sum all embeddings
        summed_emb = w_emb + jnp.broadcast_to(p_emb, w_emb.shape) + t_emb

        # Layer Norm
        layer_norm = FlaxBertLayerNorm(name="layer_norm")(summed_emb)

        return layer_norm
