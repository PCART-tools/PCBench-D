    def __init__(self, config):
        super().__init__(config)

        self.transformer = SqueezeBertModel(config)
        self.lm_head = nn.Linear(config.embedding_size, config.vocab_size)

        self.init_weights()
