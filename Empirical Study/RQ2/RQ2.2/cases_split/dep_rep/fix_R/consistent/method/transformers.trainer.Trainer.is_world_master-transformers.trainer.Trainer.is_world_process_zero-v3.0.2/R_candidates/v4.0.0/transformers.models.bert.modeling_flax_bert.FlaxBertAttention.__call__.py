    @nn.compact
    def __call__(self, hidden_state, attention_mask):
        # Attention mask comes in as attention_mask.shape == (*batch_sizes, kv_length)
        # FLAX expects: attention_mask.shape == (*batch_sizes, 1, 1, kv_length) such that it is broadcastable
        # with attn_weights.shape == (*batch_sizes, num_heads, q_length, kv_length)
        attention_mask = jnp.expand_dims(attention_mask, axis=(-3, -2))
        self_att = nn.attention.SelfAttention(num_heads=self.num_heads, qkv_features=self.head_size, name="self")(
            hidden_state, attention_mask
        )

        layer_norm = FlaxBertLayerNorm(name="layer_norm")(self_att + hidden_state)
        return layer_norm
