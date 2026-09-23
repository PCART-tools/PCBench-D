    def __init__(self, config):
        super().__init__()
        self.attention = LxmertSelfAttentionLayer(config)
        self.intermediate = LxmertIntermediate(config)
        self.output = LxmertOutput(config)
