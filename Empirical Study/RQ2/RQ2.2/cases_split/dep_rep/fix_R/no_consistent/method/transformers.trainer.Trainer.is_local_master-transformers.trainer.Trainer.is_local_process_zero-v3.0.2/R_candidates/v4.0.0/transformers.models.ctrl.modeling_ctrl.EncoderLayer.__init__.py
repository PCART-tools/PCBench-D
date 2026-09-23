    def __init__(self, d_model_size, num_heads, dff, rate=0.1):
        super().__init__()

        self.multi_head_attention = MultiHeadAttention(d_model_size, num_heads)
        self.ffn = point_wise_feed_forward_network(d_model_size, dff)

        self.layernorm1 = torch.nn.LayerNorm(d_model_size, eps=1e-6)
        self.layernorm2 = torch.nn.LayerNorm(d_model_size, eps=1e-6)

        self.dropout1 = torch.nn.Dropout(rate)
        self.dropout2 = torch.nn.Dropout(rate)
