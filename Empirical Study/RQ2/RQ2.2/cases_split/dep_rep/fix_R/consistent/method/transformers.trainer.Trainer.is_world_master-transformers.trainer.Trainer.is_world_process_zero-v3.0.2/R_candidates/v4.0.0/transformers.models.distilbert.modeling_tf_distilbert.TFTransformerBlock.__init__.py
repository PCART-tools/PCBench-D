    def __init__(self, config, **kwargs):
        super().__init__(**kwargs)

        self.n_heads = config.n_heads
        self.dim = config.dim
        self.hidden_dim = config.hidden_dim
        self.dropout = tf.keras.layers.Dropout(config.dropout)
        self.activation = config.activation
        self.output_attentions = config.output_attentions

        assert (
            config.dim % config.n_heads == 0
        ), f"Hidden size {config.dim} not dividable by number of heads {config.n_heads}"

        self.attention = TFMultiHeadSelfAttention(config, name="attention")
        self.sa_layer_norm = tf.keras.layers.LayerNormalization(epsilon=1e-12, name="sa_layer_norm")

        self.ffn = TFFFN(config, name="ffn")
        self.output_layer_norm = tf.keras.layers.LayerNormalization(epsilon=1e-12, name="output_layer_norm")
