    def __init__(self, config):
        super().__init__()
        self.att = LxmertAttention(config)
        self.output = LxmertAttentionOutput(config)
