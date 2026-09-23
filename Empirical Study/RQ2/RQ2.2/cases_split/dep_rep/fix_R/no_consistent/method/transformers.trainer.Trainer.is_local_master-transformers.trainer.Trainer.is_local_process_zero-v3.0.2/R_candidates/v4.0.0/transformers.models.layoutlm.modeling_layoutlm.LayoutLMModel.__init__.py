    def __init__(self, config):
        super(LayoutLMModel, self).__init__(config)
        self.config = config

        self.embeddings = LayoutLMEmbeddings(config)
        self.encoder = LayoutLMEncoder(config)
        self.pooler = LayoutLMPooler(config)

        self.init_weights()
