    def __init__(self, config, **kwargs):
        super().__init__(**kwargs)
        self.att = TFLxmertAttention(config, name="att")
        self.attention_output = TFLxmertAttentionOutput(config, name="output")
