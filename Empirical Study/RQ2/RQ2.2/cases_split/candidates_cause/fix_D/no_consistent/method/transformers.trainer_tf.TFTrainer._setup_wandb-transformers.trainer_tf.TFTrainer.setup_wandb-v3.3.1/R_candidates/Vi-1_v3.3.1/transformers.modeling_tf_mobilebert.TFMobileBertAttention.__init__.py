    def __init__(self, config, **kwargs):
        super().__init__(**kwargs)
        self.self = TFMobileBertSelfAttention(config, name="self")
        self.mobilebert_output = TFMobileBertSelfOutput(config, name="output")
