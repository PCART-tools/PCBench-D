    def __init__(self, config, input_embeddings, **kwargs):
        super().__init__(**kwargs)

        self.predictions = TFLxmertLMPredictionHead(config, input_embeddings, name="predictions")
