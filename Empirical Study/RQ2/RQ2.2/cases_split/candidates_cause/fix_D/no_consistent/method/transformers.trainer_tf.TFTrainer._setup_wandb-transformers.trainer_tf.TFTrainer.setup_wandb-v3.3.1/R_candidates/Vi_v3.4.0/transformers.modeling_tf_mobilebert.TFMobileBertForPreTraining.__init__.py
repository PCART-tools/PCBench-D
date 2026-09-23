    def __init__(self, config, *inputs, **kwargs):
        super().__init__(config, *inputs, **kwargs)
        self.mobilebert = TFMobileBertMainLayer(config, name="mobilebert")
        self.predictions = TFMobileBertMLMHead(config, name="predictions___cls")
        self.seq_relationship = TFMobileBertOnlyNSPHead(2, name="seq_relationship___cls")
