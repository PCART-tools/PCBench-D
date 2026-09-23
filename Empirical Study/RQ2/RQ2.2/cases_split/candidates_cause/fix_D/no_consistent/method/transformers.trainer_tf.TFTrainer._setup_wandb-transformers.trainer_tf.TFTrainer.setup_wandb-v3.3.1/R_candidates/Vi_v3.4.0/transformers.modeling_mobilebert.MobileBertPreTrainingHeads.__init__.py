    def __init__(self, config):
        super().__init__()
        self.predictions = MobileBertLMPredictionHead(config)
        self.seq_relationship = nn.Linear(config.hidden_size, 2)
