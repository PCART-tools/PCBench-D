    def __init__(self, config):
        super().__init__()
        self.linear_1 = nn.Linear(config.d_model, config.d_inner)
        self.activation_function = ACT2FN[config.hidden_act]
        self.activation_dropout = nn.Dropout(config.activation_dropout)
        self.linear_2 = nn.Linear(config.d_inner, config.d_model)
        self.dropout = nn.Dropout(config.hidden_dropout)
        self.layer_norm = nn.LayerNorm(config.d_model, config.layer_norm_eps)
