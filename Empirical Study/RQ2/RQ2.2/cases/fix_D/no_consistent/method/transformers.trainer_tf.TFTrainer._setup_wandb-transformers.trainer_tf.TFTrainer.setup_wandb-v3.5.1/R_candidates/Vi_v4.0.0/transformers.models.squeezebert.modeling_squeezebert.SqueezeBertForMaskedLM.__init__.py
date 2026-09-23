    def __init__(self, config):
        super().__init__(config)

        self.transformer = SqueezeBertModel(config)
        self.cls = SqueezeBertOnlyMLMHead(config)

        self.init_weights()
