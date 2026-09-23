    def __init__(self, config, lxmert_model_embedding_weights):
        super(LxmertPreTrainingHeads, self).__init__()
        self.predictions = LxmertLMPredictionHead(config, lxmert_model_embedding_weights)
        self.seq_relationship = nn.Linear(config.hidden_size, 2)
