    def __init__(self, config: ProphetNetConfig, word_embeddings: nn.Embedding = None):
        super().__init__(config)

        self.ngram = config.ngram
        self.num_buckets = config.num_buckets
        self.relative_max_distance = config.relative_max_distance
        self.dropout = config.dropout
        self.max_target_positions = config.max_position_embeddings

        self.word_embeddings = (
            word_embeddings
            if word_embeddings is not None
            else nn.Embedding(config.vocab_size, config.hidden_size, padding_idx=config.pad_token_id)
        )
        self.position_embeddings = ProhpetNetPositionalEmbeddings(config)

        self.ngram_embeddings = nn.Embedding(self.ngram, config.hidden_size, None)
        self.layers = nn.ModuleList([ProphetNetDecoderLayer(config) for _ in range(config.num_decoder_layers)])
        self.embeddings_layer_norm = ProphetNetLayerNorm(config.hidden_size)

        self.init_weights()
