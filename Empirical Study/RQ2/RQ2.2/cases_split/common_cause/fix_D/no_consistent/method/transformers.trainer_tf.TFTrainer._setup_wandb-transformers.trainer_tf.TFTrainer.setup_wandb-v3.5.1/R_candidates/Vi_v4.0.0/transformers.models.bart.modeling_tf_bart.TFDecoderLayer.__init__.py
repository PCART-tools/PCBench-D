    def __init__(self, config: BartConfig, **kwargs):
        super().__init__(**kwargs)
        self.embed_dim = config.d_model
        self.self_attn = TFAttention(
            embed_dim=self.embed_dim,
            num_heads=config.decoder_attention_heads,
            dropout=config.attention_dropout,
            name="self_attn",
        )
        self.dropout = config.dropout
        self.activation_fn = ACT2FN[config.activation_function]
        self.activation_dropout = config.activation_dropout
        self.normalize_before = config.normalize_before

        self.self_attn_layer_norm = LayerNormalization(epsilon=1e-5, name="self_attn_layer_norm")
        self.encoder_attn = TFAttention(
            self.embed_dim,
            config.decoder_attention_heads,
            dropout=config.attention_dropout,
            encoder_decoder_attention=True,
            name="encoder_attn",
        )
        self.encoder_attn_layer_norm = LayerNormalization(epsilon=1e-5, name="encoder_attn_layer_norm")
        self.fc1 = Dense(config.decoder_ffn_dim, name="fc1")
        self.fc2 = Dense(self.embed_dim, name="fc2")
        self.final_layer_norm = LayerNormalization(epsilon=1e-5, name="final_layer_norm")
