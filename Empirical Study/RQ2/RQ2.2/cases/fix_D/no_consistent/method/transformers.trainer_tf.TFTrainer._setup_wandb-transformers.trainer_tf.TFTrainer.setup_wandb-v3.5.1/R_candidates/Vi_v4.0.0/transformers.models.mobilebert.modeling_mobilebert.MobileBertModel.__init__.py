    def __init__(self, config, add_pooling_layer=True):
        super().__init__(config)
        self.config = config
        self.embeddings = MobileBertEmbeddings(config)
        self.encoder = MobileBertEncoder(config)

        self.pooler = MobileBertPooler(config) if add_pooling_layer else None

        self.init_weights()
