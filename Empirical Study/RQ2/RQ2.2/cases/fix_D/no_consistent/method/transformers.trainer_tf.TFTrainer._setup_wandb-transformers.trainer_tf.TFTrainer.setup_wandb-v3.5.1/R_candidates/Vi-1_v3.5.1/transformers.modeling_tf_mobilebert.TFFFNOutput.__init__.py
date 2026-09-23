    def __init__(self, config, **kwargs):
        super().__init__(**kwargs)
        self.dense = tf.keras.layers.Dense(config.true_hidden_size, name="dense")
        self.LayerNorm = NORM2FN[config.normalization_type](
            config.true_hidden_size, epsilon=config.layer_norm_eps, name="LayerNorm"
        )
