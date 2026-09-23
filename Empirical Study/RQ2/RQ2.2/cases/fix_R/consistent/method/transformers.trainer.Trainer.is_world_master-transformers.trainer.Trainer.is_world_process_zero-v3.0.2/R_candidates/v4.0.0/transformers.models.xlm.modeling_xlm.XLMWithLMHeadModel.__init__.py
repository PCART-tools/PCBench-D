    def __init__(self, config):
        super().__init__(config)
        self.transformer = XLMModel(config)
        self.pred_layer = XLMPredLayer(config)

        self.init_weights()
