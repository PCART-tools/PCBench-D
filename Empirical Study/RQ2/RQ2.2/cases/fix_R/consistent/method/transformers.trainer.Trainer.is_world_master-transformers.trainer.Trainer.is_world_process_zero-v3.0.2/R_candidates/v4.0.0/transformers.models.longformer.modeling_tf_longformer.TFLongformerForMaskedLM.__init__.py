    def __init__(self, config, *inputs, **kwargs):
        super().__init__(config, *inputs, **kwargs)

        self.longformer = TFLongformerMainLayer(config, name="longformer")
        self.lm_head = TFLongformerLMHead(config, self.longformer.embeddings, name="lm_head")
