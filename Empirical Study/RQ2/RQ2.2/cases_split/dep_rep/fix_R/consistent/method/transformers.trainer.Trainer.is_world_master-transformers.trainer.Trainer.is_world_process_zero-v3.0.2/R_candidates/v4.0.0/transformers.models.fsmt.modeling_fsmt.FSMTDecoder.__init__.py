    def __init__(self, config: FSMTConfig, embed_tokens: nn.Embedding):
        super().__init__()
        self.dropout = config.dropout
        self.layerdrop = config.decoder_layerdrop
        self.padding_idx = embed_tokens.padding_idx
        self.embed_scale = math.sqrt(config.d_model) if config.scale_embedding else 1.0
        self.embed_tokens = embed_tokens
        embed_dim = embed_tokens.embedding_dim
        self.embed_positions = SinusoidalPositionalEmbedding(
            config.max_position_embeddings + self.padding_idx + 1, embed_dim, self.padding_idx
        )
        self.layers = nn.ModuleList(
            [DecoderLayer(config) for _ in range(config.decoder_layers)]
        )  # type: List[DecoderLayer]

        self.output_projection = nn.Linear(
            self.embed_tokens.weight.shape[1],
            self.embed_tokens.weight.shape[0],
            bias=False,
        )
        self.output_projection.weight = self.embed_tokens.weight
