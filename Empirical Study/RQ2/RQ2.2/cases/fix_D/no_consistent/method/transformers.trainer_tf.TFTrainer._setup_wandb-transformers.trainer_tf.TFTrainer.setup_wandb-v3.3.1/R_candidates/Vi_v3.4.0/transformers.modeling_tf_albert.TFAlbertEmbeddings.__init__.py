    def __init__(self, config, **kwargs):
        super().__init__(**kwargs)

        self.config = config
        self.vocab_size = config.vocab_size
        self.position_embeddings = tf.keras.layers.Embedding(
            config.max_position_embeddings,
            config.embedding_size,
            embeddings_initializer=get_initializer(self.config.initializer_range),
            name="position_embeddings",
        )
        self.token_type_embeddings = tf.keras.layers.Embedding(
            config.type_vocab_size,
            config.embedding_size,
            embeddings_initializer=get_initializer(self.config.initializer_range),
            name="token_type_embeddings",
        )

        # self.LayerNorm is not snake-cased to stick with TensorFlow model variable name and be able to load
        # any TensorFlow checkpoint file
        self.LayerNorm = tf.keras.layers.LayerNormalization(epsilon=config.layer_norm_eps, name="LayerNorm")
        self.dropout = tf.keras.layers.Dropout(config.hidden_dropout_prob)
