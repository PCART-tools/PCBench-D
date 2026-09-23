    def __init__(self, config, **kwargs):
        super().__init__(**kwargs)

        self.self_attention = TFRobertaSelfAttention(config, name="self")
        self.dense_output = TFRobertaSelfOutput(config, name="output")
