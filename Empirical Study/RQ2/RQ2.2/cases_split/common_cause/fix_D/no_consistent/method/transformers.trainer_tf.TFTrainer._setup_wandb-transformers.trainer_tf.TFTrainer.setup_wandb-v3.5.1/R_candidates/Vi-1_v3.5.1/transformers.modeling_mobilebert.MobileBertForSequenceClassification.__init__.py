    def __init__(self, config):
        super().__init__(config)
        self.num_labels = config.num_labels
        self.mobilebert = MobileBertModel(config)
        self.dropout = nn.Dropout(config.hidden_dropout_prob)
        self.classifier = nn.Linear(config.hidden_size, self.num_labels)

        self.init_weights()
