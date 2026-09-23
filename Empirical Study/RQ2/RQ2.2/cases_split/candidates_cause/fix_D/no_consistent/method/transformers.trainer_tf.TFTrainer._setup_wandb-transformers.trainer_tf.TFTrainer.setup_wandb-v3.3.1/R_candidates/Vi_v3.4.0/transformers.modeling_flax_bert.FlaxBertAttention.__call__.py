    @compact
    def __call__(self, hidden_state, attention_mask):
        self_att = nn.attention.SelfAttention(num_heads=self.num_heads, qkv_features=self.head_size, name="self")(
            hidden_state, attention_mask
        )

        layer_norm = FlaxBertLayerNorm(name="layer_norm")(self_att + hidden_state)
        return layer_norm
