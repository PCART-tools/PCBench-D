@tensorrt_converter(acc_ops.max_dim_reduce)
def acc_ops_max_dim_reduce(network, target, args, kwargs, name):
    return add_acc_ops_dim_reduce(network, target, args, kwargs, name, trt.ReduceOperation.MAX)
