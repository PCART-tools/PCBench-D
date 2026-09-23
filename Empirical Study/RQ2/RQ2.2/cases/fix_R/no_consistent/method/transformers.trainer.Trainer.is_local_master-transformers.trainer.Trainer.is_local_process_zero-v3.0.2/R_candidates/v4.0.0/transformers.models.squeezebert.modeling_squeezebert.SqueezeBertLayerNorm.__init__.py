    def __init__(self, hidden_size, eps=1e-12):
        nn.LayerNorm.__init__(self, normalized_shape=hidden_size, eps=eps)  # instantiates self.{weight, bias, eps}
