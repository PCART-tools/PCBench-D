    def __init__(self, config, *inputs, **kwargs):
        super().__init__(config, *inputs, **kwargs)
        self.vocab_size = config.vocab_size

        self.distilbert = TFDistilBertMainLayer(config, name="distilbert")
        self.vocab_transform = tf.keras.layers.Dense(
            config.dim, kernel_initializer=get_initializer(config.initializer_range), name="vocab_transform"
        )
        self.act = get_tf_activation("gelu")
        self.vocab_layer_norm = tf.keras.layers.LayerNormalization(epsilon=1e-12, name="vocab_layer_norm")
        self.vocab_projector = TFDistilBertLMHead(config, self.distilbert.embeddings, name="vocab_projector")
