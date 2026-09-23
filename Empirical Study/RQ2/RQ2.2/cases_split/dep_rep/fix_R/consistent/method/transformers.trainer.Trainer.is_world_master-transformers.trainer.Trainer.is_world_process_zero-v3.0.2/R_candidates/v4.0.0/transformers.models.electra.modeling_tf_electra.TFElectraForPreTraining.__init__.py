    def __init__(self, config, **kwargs):
        super().__init__(config, **kwargs)

        self.electra = TFElectraMainLayer(config, name="electra")
        self.discriminator_predictions = TFElectraDiscriminatorPredictions(config, name="discriminator_predictions")
