    def __init__(self, config):
        super().__init__(config)

        self.funnel = FunnelBaseModel(config)
        self.classifier = FunnelClassificationHead(config, 1)
        self.init_weights()
