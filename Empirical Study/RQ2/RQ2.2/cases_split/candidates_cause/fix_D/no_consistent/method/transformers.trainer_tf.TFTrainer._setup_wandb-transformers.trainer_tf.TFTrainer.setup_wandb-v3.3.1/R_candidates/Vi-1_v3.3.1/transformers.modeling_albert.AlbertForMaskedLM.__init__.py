    def __init__(self, config):
        super().__init__(config)

        self.albert = AlbertModel(config, add_pooling_layer=False)
        self.predictions = AlbertMLMHead(config)

        self.init_weights()
