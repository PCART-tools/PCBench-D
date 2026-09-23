    def __init__(self, config, **kwargs):
        super().__init__(**kwargs)
        if config.feed_forward_proj == "relu":
            self.DenseReluDense = TFT5DenseReluDense(config, name="DenseReluDense")
        elif config.feed_forward_proj == "gated-gelu":
            self.DenseReluDense = TFT5GatedGeluDense(config, name="DenseReluDense")
        else:
            raise ValueError(
                f"{self.config.feed_forward_proj} is not supported. Choose between `relu` and `gated-gelu`"
            )
        self.layer_norm = TFT5LayerNorm(epsilon=config.layer_norm_epsilon, name="layer_norm")
        self.dropout = tf.keras.layers.Dropout(config.dropout_rate)
