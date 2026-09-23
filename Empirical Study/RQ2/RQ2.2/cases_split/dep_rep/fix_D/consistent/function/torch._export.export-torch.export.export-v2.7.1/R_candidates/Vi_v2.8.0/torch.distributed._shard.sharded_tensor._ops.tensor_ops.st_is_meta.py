@_sharded_op_impl(torch.Tensor.is_meta.__get__)  # type: ignore[attr-defined]
def st_is_meta(types, args=(), kwargs=None, pg=None):
    return args[0].local_tensor().is_meta
