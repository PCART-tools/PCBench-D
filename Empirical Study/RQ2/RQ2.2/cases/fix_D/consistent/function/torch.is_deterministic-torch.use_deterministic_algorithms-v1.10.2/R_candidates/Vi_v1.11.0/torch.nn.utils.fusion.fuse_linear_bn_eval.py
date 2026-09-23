def fuse_linear_bn_eval(linear, bn):
    assert(not (linear.training or bn.training)), "Fusion only for eval!"
    fused_linear = copy.deepcopy(linear)

    fused_linear.weight, fused_linear.bias = fuse_linear_bn_weights(
        fused_linear.weight, fused_linear.bias,
        bn.running_mean, bn.running_var, bn.eps, bn.weight, bn.bias)

    return fused_linear
