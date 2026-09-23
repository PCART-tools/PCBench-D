def fuse_linear_bn(is_qat, linear, bn):
    r"""Given the linear and bn modules, fuses them and returns the fused module

    Args:
        is_qat: a flag for whether we are using quantization aware training fusion
        or post training quantization fusion
        linear: Module instance of type Linear
        bn: BatchNorm1d instance that needs to be fused with the linear layer

    Examples::

        >>> m1 = nn.Linear(20, 10)
        >>> b1 = nn.BatchNorm1d(10)
        >>> m2 = fuse_linear_bn(m1, b1)
    """
    assert(linear.training == bn.training),\
        "Linear and BN both must be in the same mode (train or eval)."

    if is_qat:
        # TODO: remove the assert later
        assert linear.training, "qat is only supported when linear.training is True currently"
        raise Exception("Fusing Linear+BatchNorm not yet supported in training.")
    else:
        return nn.utils.fusion.fuse_linear_bn_eval(linear, bn)
