    def __init__(self, config):
        super().__init__(config)

        self.embeddings = SqueezeBertEmbeddings(config)
        self.encoder = SqueezeBertEncoder(config)
        self.pooler = SqueezeBertPooler(config)

        self.init_weights()
