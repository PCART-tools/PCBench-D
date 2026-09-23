    def __init__(self, config, *inputs, **kwargs):
        super().__init__(config, *inputs, **kwargs)

        self.funnel = TFFunnelMainLayer(config, name="funnel")
        self.lm_head = TFFunnelMaskedLMHead(config, self.funnel.embeddings, name="lm_head")
