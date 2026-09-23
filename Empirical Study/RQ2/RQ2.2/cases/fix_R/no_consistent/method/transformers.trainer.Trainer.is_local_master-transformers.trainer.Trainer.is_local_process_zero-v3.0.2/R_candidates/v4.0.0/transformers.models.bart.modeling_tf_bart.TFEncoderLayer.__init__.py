    def __init__(self, config: BartConfig, **kwargs):
        super().__init__(**kwargs)
        self.embed_dim = config.d_model
        self.self_attn = TFAttention(
            self.embed_dim, config.encoder_attention_heads, dropout=config.attention_dropout, name="self_attn"
        )
        self.normalize_before = config.normalize_before
        self.self_attn_layer_norm = LayerNormalization(epsilon=1e-5, name="self_attn_layer_norm")
        self.dropout = config.dropout
        self.activation_fn = ACT2FN[config.activation_function]
        self.activation_dropout = config.activation_dropout
        self.fc1 = Dense(config.encoder_ffn_dim, name="fc1")
        self.fc2 = Dense(self.embed_dim, name="fc2")
        self.final_layer_norm = LayerNormalization(epsilon=1e-5, name="final_layer_norm")
