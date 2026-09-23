def relu_inplace_method_replacement(x, scale, zero_point):
    x = x.relu_()
    return x
