@_sharded_op_impl(torch.allclose)
def allclose(types, args, kwargs, process_group):
    return binary_cmp(torch.allclose, types, args, kwargs, process_group)
