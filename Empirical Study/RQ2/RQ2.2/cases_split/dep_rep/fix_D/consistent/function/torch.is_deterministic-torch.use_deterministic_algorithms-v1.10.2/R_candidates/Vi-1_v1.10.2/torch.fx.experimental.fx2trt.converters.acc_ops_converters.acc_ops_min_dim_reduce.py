@tensorrt_converter(acc_ops.min_dim_reduce)
def acc_ops_min_dim_reduce(network, target, args, kwargs, name):
    return add_acc_ops_dim_reduce(network, target, args, kwargs, name, trt.ReduceOperation.MIN)
