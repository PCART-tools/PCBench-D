def _initialize_orthogonal(conv):
    prelu_gain = math.sqrt(2)
    init.orthogonal(conv.weight, gain=prelu_gain)
    if conv.bias is not None:
        conv.bias.data.zero_()
