    def __init__(self, config, *inputs, **kwargs):
        super().__init__(config, *inputs, **kwargs)

        self.mobilebert = TFMobileBertMainLayer(config, name="mobilebert")
        self.mlm = TFMobileBertMLMHead(config, name="mlm___cls")
