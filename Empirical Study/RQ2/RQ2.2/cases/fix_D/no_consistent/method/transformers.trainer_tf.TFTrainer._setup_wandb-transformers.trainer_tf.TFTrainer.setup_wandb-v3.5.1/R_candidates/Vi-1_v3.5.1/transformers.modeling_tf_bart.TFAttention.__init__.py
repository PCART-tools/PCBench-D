    def __init__(
        self,
        embed_dim,
        num_heads,
        dropout=0.0,
        bias=True,
        encoder_decoder_attention=False,  # otherwise self_attention
        **kwargs,
    ):
        super().__init__(**kwargs)
        self.embed_dim = embed_dim

        self.num_heads = num_heads
        self.dropout = dropout
        self.head_dim = embed_dim // num_heads
        assert self.head_dim * num_heads == self.embed_dim, "embed_dim must be divisible by num_heads"
        self.scaling = self.head_dim ** -0.5

        self.encoder_decoder_attention = encoder_decoder_attention

        self.k_proj = Dense(embed_dim, use_bias=bias, name="k_proj")
        self.q_proj = Dense(embed_dim, use_bias=bias, name="q_proj")
        self.v_proj = Dense(embed_dim, use_bias=bias, name="v_proj")
        self.out_proj = Dense(embed_dim, use_bias=bias, name="out_proj")

        self.cache_key = "encoder_decoder" if self.encoder_decoder_attention else "self"
