    def __init__(self, config, **kwargs):
        super().__init__(**kwargs)
        self.use_bottleneck = config.use_bottleneck
        self.num_feedforward_networks = config.num_feedforward_networks
        self.attention = TFMobileBertAttention(config, name="attention")
        self.intermediate = TFMobileBertIntermediate(config, name="intermediate")
        self.mobilebert_output = TFMobileBertOutput(config, name="output")

        if self.use_bottleneck:
            self.bottleneck = TFBottleneck(config, name="bottleneck")
        if config.num_feedforward_networks > 1:
            self.ffn = [
                TFFFNLayer(config, name="ffn.{}".format(i)) for i in range(config.num_feedforward_networks - 1)
            ]
