    def __init__(self, config, **kwargs):
        super().__init__(**kwargs)
        self.self = TFLxmertAttention(config, name="self")
        self.attention_output = TFLxmertAttentionOutput(config, name="output")
