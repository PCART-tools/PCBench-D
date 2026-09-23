    def __init__(self, config: ProphetNetConfig):
        super().__init__()
        # 1st residual block
        self.self_attn = ProphetNetSelfAttention(config, config.num_encoder_attention_heads)
        self.self_attn_layer_norm = ProphetNetLayerNorm(config.hidden_size)

        # 2nd residual block
        self.feed_forward = ProhpetNetFeedForward(config, config.encoder_ffn_dim)
        self.feed_forward_layer_norm = ProphetNetLayerNorm(config.hidden_size)
