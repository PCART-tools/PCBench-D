def _acc_func(opname, x):
    if opname == "Swish":
        return _swish(x)
    elif opname == "Sigmoid":
        return _sigmoid(x)
    elif opname == "Tanh":
        return _tanh(x)
    elif opname == "Gelu":
        return _gelu_by_sigmoid(x)
    else:
        return x
