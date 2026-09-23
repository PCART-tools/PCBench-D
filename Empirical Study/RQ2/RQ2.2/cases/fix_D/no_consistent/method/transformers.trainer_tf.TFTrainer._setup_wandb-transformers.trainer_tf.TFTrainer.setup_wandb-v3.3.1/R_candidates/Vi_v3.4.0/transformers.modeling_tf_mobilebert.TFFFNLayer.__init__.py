    def __init__(self, config, **kwargs):
        super().__init__(**kwargs)
        self.intermediate = TFMobileBertIntermediate(config, name="intermediate")
        self.mobilebert_output = TFFFNOutput(config, name="output")
