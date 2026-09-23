    def __init__(self, config: ProphetNetConfig, word_embeddings: nn.Embedding = None):
        super().__init__(config)

        self.word_embeddings = (
            word_embeddings
            if word_embeddings is not None
            else nn.Embedding(config.vocab_size, config.hidden_size, padding_idx=config.pad_token_id)
        )
        self.position_embeddings = ProhpetNetPositionalEmbeddings(config)
        self.embeddings_layer_norm = ProphetNetLayerNorm(config.hidden_size)

        self.layers = nn.ModuleList([ProphetNetEncoderLayer(config) for _ in range(config.num_encoder_layers)])

        self.init_weights()
