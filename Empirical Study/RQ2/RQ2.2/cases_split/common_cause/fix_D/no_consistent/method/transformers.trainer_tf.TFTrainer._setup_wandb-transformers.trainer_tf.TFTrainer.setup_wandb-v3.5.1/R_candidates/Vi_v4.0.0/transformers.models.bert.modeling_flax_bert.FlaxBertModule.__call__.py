    @nn.compact
    def __call__(self, input_ids, attention_mask, token_type_ids, position_ids):

        # Embedding
        embeddings = FlaxBertEmbeddings(
            self.vocab_size, self.hidden_size, self.type_vocab_size, self.max_length, name="embeddings"
        )(input_ids, token_type_ids, position_ids, attention_mask)

        # N stacked encoding layers
        encoder = FlaxBertEncoder(
            self.num_encoder_layers, self.num_heads, self.head_size, self.intermediate_size, name="encoder"
        )(embeddings, attention_mask)

        pooled = FlaxBertPooler(name="pooler")(encoder)
        return encoder, pooled
