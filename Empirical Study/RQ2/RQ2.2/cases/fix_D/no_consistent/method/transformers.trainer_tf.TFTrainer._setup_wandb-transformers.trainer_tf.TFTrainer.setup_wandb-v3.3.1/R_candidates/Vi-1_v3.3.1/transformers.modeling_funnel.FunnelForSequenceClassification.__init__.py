    def __init__(self, config):
        super().__init__(config)
        self.num_labels = config.num_labels

        self.funnel = FunnelBaseModel(config)
        self.classifier = FunnelClassificationHead(config, config.num_labels)
        self.init_weights()
