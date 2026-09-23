    def __init__(self, config, has_relative_attention_bias=False, **kwargs):
        super().__init__(**kwargs)
        self.EncDecAttention = TFT5Attention(
            config,
            has_relative_attention_bias=has_relative_attention_bias,
            name="EncDecAttention",
        )
        self.layer_norm = TFT5LayerNorm(epsilon=config.layer_norm_epsilon, name="layer_norm")
        self.dropout = tf.keras.layers.Dropout(config.dropout_rate)
