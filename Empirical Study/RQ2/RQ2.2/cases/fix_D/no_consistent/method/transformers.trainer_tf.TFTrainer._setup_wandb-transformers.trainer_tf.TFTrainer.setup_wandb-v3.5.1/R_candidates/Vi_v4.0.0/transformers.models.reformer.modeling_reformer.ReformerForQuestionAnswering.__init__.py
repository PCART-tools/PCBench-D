    def __init__(self, config):
        super().__init__(config)
        self.num_labels = config.num_labels

        self.reformer = ReformerModel(config)
        # 2 * config.hidden_size because we use reversible residual layers
        self.qa_outputs = nn.Linear(2 * config.hidden_size, config.num_labels)

        self.init_weights()
