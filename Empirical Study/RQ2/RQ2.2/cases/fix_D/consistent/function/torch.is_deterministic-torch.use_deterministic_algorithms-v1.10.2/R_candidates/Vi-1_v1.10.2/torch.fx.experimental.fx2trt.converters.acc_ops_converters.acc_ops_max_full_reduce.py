@tensorrt_converter(acc_ops.max_full_reduce)
def acc_ops_max_full_reduce(network, target, args, kwargs, name):
    return add_acc_ops_full_reduce(network, target, args, kwargs, name, trt.ReduceOperation.MAX)
