    def __init__(self, cin, cout, groups, dropout_prob):
        super().__init__()

        self.conv1d = nn.Conv1d(in_channels=cin, out_channels=cout, kernel_size=1, groups=groups)
        self.layernorm = SqueezeBertLayerNorm(cout)
        self.dropout = nn.Dropout(dropout_prob)
