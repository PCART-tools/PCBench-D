    def __init__(self, config):
        super().__init__(config)
        self.config = config

        self.embeddings = BertGenerationEmbeddings(config)
        self.encoder = BertEncoder(config)

        self.init_weights()
