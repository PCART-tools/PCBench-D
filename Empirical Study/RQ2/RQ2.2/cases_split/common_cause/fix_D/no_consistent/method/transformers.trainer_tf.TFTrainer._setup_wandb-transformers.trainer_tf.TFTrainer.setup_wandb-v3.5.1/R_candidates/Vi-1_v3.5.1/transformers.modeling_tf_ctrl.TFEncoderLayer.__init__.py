    def __init__(
        self, d_model_size, num_heads, dff, rate=0.1, layer_norm_epsilon=1e-6, output_attentions=False, **kwargs
    ):
        super().__init__(**kwargs)

        self.output_attentions = output_attentions

        self.multi_head_attention = TFMultiHeadAttention(
            d_model_size, num_heads, output_attentions=self.output_attentions, name="multi_head_attention"
        )
        self.ffn = TFPointWiseFeedForwardLayer(d_model_size, dff, name="ffn")

        self.layernorm1 = tf.keras.layers.LayerNormalization(epsilon=layer_norm_epsilon, name="layernorm1")
        self.layernorm2 = tf.keras.layers.LayerNormalization(epsilon=layer_norm_epsilon, name="layernorm2")

        self.dropout1 = tf.keras.layers.Dropout(rate)
        self.dropout2 = tf.keras.layers.Dropout(rate)
