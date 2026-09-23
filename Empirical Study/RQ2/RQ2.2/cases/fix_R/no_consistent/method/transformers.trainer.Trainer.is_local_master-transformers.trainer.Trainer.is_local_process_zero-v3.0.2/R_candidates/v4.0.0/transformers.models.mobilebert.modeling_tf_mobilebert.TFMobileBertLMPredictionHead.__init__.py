    def __init__(self, config, **kwargs):
        super().__init__(**kwargs)
        self.transform = TFMobileBertPredictionHeadTransform(config, name="transform")
        self.vocab_size = config.vocab_size
        self.config = config
