    def __init__(self, config: ProphetNetConfig):
        super().__init__()
        # 1st residual block
        self.self_attn = ProphetNetNgramProphetNetSelfAttention(config)
        self.self_attn_layer_norm = ProphetNetLayerNorm(config.hidden_size)

        # 2nd residual block
        if config.add_cross_attention:
            self.cross_attn = ProphetNetSelfAttention(config, config.num_decoder_attention_heads)
            self.cross_attn_layer_norm = ProphetNetLayerNorm(config.hidden_size)

        # 3rd residual block
        self.feed_forward = ProhpetNetFeedForward(config, config.decoder_ffn_dim)
        self.feed_forward_layer_norm = ProphetNetLayerNorm(config.hidden_size)
