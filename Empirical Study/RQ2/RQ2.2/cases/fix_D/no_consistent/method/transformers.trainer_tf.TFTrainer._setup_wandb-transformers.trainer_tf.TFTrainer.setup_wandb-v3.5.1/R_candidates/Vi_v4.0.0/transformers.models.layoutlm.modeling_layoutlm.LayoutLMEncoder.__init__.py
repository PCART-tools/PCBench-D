    def __init__(self, config):
        super().__init__()
        self.config = config
        self.layer = nn.ModuleList([LayoutLMLayer(config) for _ in range(config.num_hidden_layers)])
