    def __init__(self, config, **kwargs):
        super().__init__(**kwargs)
        self.trigram_input = config.trigram_input
        self.embedding_size = config.embedding_size
        self.vocab_size = config.vocab_size
        self.hidden_size = config.hidden_size
        self.initializer_range = config.initializer_range

        self.position_embeddings = tf.keras.layers.Embedding(
            config.max_position_embeddings,
            config.hidden_size,
            embeddings_initializer=get_initializer(self.initializer_range),
            name="position_embeddings",
        )
        self.token_type_embeddings = tf.keras.layers.Embedding(
            config.type_vocab_size,
            config.hidden_size,
            embeddings_initializer=get_initializer(self.initializer_range),
            name="token_type_embeddings",
        )

        self.embedding_transformation = tf.keras.layers.Dense(config.hidden_size, name="embedding_transformation")

        # self.LayerNorm is not snake-cased to stick with TensorFlow model variable name and be able to load
        # any TensorFlow checkpoint file
        self.LayerNorm = NORM2FN[config.normalization_type](
            config.hidden_size, epsilon=config.layer_norm_eps, name="LayerNorm"
        )
        self.dropout = tf.keras.layers.Dropout(config.hidden_dropout_prob)
