    def __init__(self, config, *inputs, **kwargs):
        super().__init__(config, *inputs, **kwargs)

        self.funnel = TFFunnelBaseLayer(config, name="funnel")
        self.classifier = TFFunnelClassificationHead(config, 1, name="classifier")
