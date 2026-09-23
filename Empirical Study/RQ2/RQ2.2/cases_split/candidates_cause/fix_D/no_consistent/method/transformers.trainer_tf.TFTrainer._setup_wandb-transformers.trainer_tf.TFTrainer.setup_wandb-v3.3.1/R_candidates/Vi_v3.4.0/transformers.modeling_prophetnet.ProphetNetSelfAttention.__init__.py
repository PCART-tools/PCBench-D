    def __init__(
        self,
        config: ProphetNetConfig,
        num_attn_heads: int,
    ):
        super().__init__()
        hidden_size = config.hidden_size

        self.attention_dropout = config.attention_dropout
        self.dropout = config.dropout
        self.num_attn_heads = num_attn_heads
        self.head_dim = hidden_size // num_attn_heads

        assert (
            self.head_dim * num_attn_heads == hidden_size
        ), "`config.hidden_size` must be divisible by `config.num_encoder_attention_heads` and `config.num_decoder_attention_heads`"

        self.key_proj = nn.Linear(hidden_size, hidden_size)
        self.value_proj = nn.Linear(hidden_size, hidden_size)
        self.query_proj = nn.Linear(hidden_size, hidden_size)

        self.out_proj = nn.Linear(hidden_size, hidden_size)
