    def __init__(self, config, *inputs, **kwargs):
        super().__init__(config, *inputs, **kwargs)

        self.roberta = TFRobertaMainLayer(config, name="roberta")
        self.lm_head = TFRobertaLMHead(config, self.roberta.embeddings, name="lm_head")
