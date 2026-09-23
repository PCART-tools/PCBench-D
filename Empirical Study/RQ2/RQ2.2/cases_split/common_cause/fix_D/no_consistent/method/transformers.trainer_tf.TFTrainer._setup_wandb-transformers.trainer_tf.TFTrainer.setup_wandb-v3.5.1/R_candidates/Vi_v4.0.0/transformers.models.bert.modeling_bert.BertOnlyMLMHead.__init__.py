    def __init__(self, config):
        super().__init__()
        self.predictions = BertLMPredictionHead(config)
