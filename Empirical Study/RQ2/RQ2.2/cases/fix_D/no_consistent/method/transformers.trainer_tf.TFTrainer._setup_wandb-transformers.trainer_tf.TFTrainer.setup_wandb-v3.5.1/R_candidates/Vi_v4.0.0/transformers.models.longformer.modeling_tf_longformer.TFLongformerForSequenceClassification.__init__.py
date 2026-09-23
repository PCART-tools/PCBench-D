    def __init__(self, config, *inputs, **kwargs):
        super().__init__(config, *inputs, **kwargs)

        self.num_labels = config.num_labels

        self.longformer = TFLongformerMainLayer(config, name="longformer")
        self.classifier = TFLongformerClassificationHead(config, name="classifier")
