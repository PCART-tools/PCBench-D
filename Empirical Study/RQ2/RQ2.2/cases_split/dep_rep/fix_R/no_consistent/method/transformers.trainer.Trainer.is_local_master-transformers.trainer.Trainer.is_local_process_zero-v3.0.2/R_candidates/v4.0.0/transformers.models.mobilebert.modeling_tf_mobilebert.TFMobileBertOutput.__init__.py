    def __init__(self, config, **kwargs):
        super().__init__(**kwargs)
        self.use_bottleneck = config.use_bottleneck
        self.dense = tf.keras.layers.Dense(
            config.true_hidden_size, kernel_initializer=get_initializer(config.initializer_range), name="dense"
        )
        self.LayerNorm = NORM2FN[config.normalization_type](
            config.true_hidden_size, epsilon=config.layer_norm_eps, name="LayerNorm"
        )
        if not self.use_bottleneck:
            self.dropout = tf.keras.layers.Dropout(config.hidden_dropout_prob)
        else:
            self.bottleneck = TFOutputBottleneck(config, name="bottleneck")
