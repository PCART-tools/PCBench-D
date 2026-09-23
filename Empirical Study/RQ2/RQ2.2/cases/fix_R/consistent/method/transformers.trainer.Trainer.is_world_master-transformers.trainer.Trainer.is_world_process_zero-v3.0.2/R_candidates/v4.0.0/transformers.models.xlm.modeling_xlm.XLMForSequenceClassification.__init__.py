    def __init__(self, config):
        super().__init__(config)
        self.num_labels = config.num_labels

        self.transformer = XLMModel(config)
        self.sequence_summary = SequenceSummary(config)

        self.init_weights()
