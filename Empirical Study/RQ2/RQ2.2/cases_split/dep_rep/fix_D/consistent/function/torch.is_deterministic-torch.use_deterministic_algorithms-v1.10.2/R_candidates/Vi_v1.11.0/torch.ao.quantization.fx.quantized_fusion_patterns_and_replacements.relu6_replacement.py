def relu6_replacement(x, scale, zero_point):
    x = torch.nn.functional.relu6(x)
    return x
