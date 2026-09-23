    def __init__(self, config, *inputs, **kwargs):
        super().__init__(config, *inputs, **kwargs)
        self.transformer = TFXLNetMainLayer(config, name="transformer")
        self.lm_loss = TFXLNetLMHead(config, self.transformer.word_embedding, name="lm_loss")
