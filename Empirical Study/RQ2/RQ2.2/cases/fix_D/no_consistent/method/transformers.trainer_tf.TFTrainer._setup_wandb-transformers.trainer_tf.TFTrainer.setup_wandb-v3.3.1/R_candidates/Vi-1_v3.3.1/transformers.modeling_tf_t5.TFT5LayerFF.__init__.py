    def __init__(self, config, **kwargs):
        super().__init__(**kwargs)
        self.DenseReluDense = TFT5DenseReluDense(config, name="DenseReluDense")
        self.layer_norm = TFT5LayerNorm(epsilon=config.layer_norm_epsilon, name="layer_norm")
        self.dropout = tf.keras.layers.Dropout(config.dropout_rate)
