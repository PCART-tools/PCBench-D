@tensorrt_converter(acc_ops.contiguous)
def acc_ops_contiguous(network, target, args, kwargs, name):
    return kwargs["input"]
