    def __init__(self, config, input_embeddings, **kwargs):
        super().__init__(**kwargs)
        self.predictions = TFLxmertLMPredictionHead(config, input_embeddings, name="predictions")

        self.seq_relationship = tf.keras.layers.Dense(
            2,
            kernel_initializer=get_initializer(config.initializer_range),
            name="seq_relationship",
        )
