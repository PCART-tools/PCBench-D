    def __init__(self, config, **kwargs):
        super().__init__(**kwargs)

        self.self_attention = TFElectraSelfAttention(config, name="self")
        self.dense_output = TFElectraSelfOutput(config, name="output")
