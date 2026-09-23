    def __init__(self, config):
        super().__init__()
        self.self = LayoutLMSelfAttention(config)
        self.output = LayoutLMSelfOutput(config)
        self.pruned_heads = set()
