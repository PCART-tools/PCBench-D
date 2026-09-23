    def __init__(self, config, **kwargs):
        super().__init__(config, **kwargs)

        self.funnel = TFFunnelMainLayer(config, name="funnel")
        self.discriminator_predictions = TFFunnelDiscriminatorPredictions(config, name="discriminator_predictions")
