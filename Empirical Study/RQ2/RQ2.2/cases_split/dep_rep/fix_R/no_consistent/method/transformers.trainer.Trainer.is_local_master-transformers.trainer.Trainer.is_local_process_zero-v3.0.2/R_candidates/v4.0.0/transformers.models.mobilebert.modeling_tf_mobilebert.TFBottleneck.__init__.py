    def __init__(self, config, **kwargs):
        super().__init__(**kwargs)
        self.key_query_shared_bottleneck = config.key_query_shared_bottleneck
        self.use_bottleneck_attention = config.use_bottleneck_attention
        self.bottleneck_input = TFBottleneckLayer(config, name="input")
        if self.key_query_shared_bottleneck:
            self.attention = TFBottleneckLayer(config, name="attention")
