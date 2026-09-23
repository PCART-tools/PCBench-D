    def __init__(self, config):
        super().__init__()
        all_head_size = config.num_attention_heads * config.attention_head_size
        self.dropout = config.hidden_dropout_prob

        self.dense = nn.Linear(all_head_size, config.hidden_size, bias=False)
