    def __init__(self, config, cin, q_groups=1, k_groups=1, v_groups=1):
        """
        config = used for some things; ignored for others (work in progress...)
        cin = input channels = output channels
        groups = number of groups to use in conv1d layers
        """
        super().__init__()
        if cin % config.num_attention_heads != 0:
            raise ValueError(
                "cin (%d) is not a multiple of the number of attention "
                "heads (%d)" % (cin, config.num_attention_heads)
            )
        self.num_attention_heads = config.num_attention_heads
        self.attention_head_size = int(cin / config.num_attention_heads)
        self.all_head_size = self.num_attention_heads * self.attention_head_size

        self.query = nn.Conv1d(in_channels=cin, out_channels=cin, kernel_size=1, groups=q_groups)
        self.key = nn.Conv1d(in_channels=cin, out_channels=cin, kernel_size=1, groups=k_groups)
        self.value = nn.Conv1d(in_channels=cin, out_channels=cin, kernel_size=1, groups=v_groups)

        self.dropout = nn.Dropout(config.attention_probs_dropout_prob)
        self.softmax = nn.Softmax(dim=-1)

        self.matmul_qk = MatMulWrapper()
        self.matmul_qkv = MatMulWrapper()
