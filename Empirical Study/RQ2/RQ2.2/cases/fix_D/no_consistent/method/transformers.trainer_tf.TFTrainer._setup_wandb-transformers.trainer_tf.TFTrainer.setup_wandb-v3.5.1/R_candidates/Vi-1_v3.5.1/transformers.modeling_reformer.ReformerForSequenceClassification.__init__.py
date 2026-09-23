    def __init__(self, config):
        super().__init__(config)
        self.num_labels = config.num_labels

        self.reformer = ReformerModel(config)
        self.classifier = ReformerClassificationHead(config)
        if config.is_decoder is True:
            logger.warning("You might want to disable causal masking for sequence classification")

        self.init_weights()
