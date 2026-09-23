    def __init__(self, config):
        super().__init__(config)

        self.embeddings = FunnelEmbeddings(config)
        self.encoder = FunnelEncoder(config)

        self.init_weights()
