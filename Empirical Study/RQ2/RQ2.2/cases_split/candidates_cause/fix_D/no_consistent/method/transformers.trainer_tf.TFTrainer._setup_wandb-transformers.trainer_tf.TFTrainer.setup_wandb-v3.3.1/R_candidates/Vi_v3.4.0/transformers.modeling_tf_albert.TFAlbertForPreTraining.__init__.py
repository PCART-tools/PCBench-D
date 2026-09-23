    def __init__(self, config, *inputs, **kwargs):
        super().__init__(config, *inputs, **kwargs)
        self.num_labels = config.num_labels

        self.albert = TFAlbertMainLayer(config, name="albert")
        self.predictions = TFAlbertMLMHead(config, self.albert.embeddings, name="predictions")
        self.sop_classifier = TFAlbertSOPHead(config, name="sop_classifier")
