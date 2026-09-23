    def __init__(self, config: ProphetNetConfig):
        super().__init__()
        self.hidden_size = config.hidden_size

        self.num_buckets = config.num_buckets
        self.relative_max_distance = config.relative_max_distance
        self.num_attn_heads = config.num_attention_heads
        self.dropout = config.dropout
        self.attention_dropout = config.attention_dropout
        self.head_dim = config.hidden_size // self.num_attn_heads
        self.ngram = config.ngram

        assert (
            self.head_dim * self.num_attn_heads == config.hidden_size
        ), "config.hidden_size must be divisible by num_attn_heads"
        # key, value, query projection
        self.key_proj = nn.Linear(config.hidden_size, config.hidden_size)
        self.value_proj = nn.Linear(config.hidden_size, config.hidden_size)
        self.query_proj = nn.Linear(config.hidden_size, config.hidden_size)

        # out projection
        self.out_proj = nn.Linear(config.hidden_size, config.hidden_size)

        # rel position embeddings
        self.relative_pos_embeddings = nn.Linear(config.hidden_size, self.num_buckets * self.num_attn_heads)

        # for onnx runtime
        self.onnx_trace = False
