    def __init__(self, config):
        super().__init__()
        self.dropout = config.hidden_dropout_prob

        if isinstance(config.hidden_act, str):
            self.act_fn = ACT2FN[config.hidden_act]
        else:
            self.act_fn = config.hidden_act

        self.dense = nn.Linear(config.hidden_size, config.feed_forward_size)
