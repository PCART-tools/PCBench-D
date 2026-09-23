    def __init__(self, config, **kwargs):
        super().__init__(**kwargs)
        self.predictions = TFMobileBertLMPredictionHead(config, name="predictions")
