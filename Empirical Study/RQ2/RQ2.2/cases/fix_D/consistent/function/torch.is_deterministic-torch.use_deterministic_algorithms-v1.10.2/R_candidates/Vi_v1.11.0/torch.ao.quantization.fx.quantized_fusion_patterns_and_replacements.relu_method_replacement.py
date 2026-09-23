def relu_method_replacement(x, scale, zero_point):
    x = x.relu()
    return x
