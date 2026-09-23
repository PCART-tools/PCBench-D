    def __init__(self, config, **kwargs):
        super().__init__(**kwargs)
        self.vocab_size = config.vocab_size
        self.dim = config.dim
        self.initializer_range = config.initializer_range
        self.word_embeddings = TFSharedEmbeddings(
            config.vocab_size, config.dim, initializer_range=config.initializer_range, name="word_embeddings"
        )  # padding_idx=0)
        self.position_embeddings = tf.keras.layers.Embedding(
            config.max_position_embeddings,
            config.dim,
            embeddings_initializer=get_initializer(config.initializer_range),
            name="position_embeddings",
        )

        self.LayerNorm = tf.keras.layers.LayerNormalization(epsilon=1e-12, name="LayerNorm")
        self.dropout = tf.keras.layers.Dropout(config.dropout)
