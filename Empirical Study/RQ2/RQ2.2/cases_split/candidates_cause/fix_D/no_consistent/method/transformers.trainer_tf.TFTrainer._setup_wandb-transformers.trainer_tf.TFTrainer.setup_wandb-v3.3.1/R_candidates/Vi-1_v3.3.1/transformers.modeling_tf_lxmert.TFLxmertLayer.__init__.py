    def __init__(self, config, **kwargs):
        super().__init__(**kwargs)
        self.attention = TFLxmertSelfAttentionLayer(config, name="attention")
        self.intermediate = TFLxmertIntermediate(config, name="intermediate")
        self.transformer_output = TFLxmertOutput(config, name="output")
