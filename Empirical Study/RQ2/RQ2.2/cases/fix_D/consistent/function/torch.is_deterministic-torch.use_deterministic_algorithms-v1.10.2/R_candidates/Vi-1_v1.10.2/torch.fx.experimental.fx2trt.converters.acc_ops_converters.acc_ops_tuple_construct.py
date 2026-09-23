@tensorrt_converter(acc_ops.tuple_construct)
def acc_ops_tuple_construct(network, target, args, kwargs, name):
    return kwargs["tensors"]
