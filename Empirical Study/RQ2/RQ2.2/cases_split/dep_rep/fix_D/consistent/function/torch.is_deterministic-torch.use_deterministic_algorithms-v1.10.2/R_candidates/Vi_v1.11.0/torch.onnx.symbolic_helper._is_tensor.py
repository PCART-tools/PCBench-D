def _is_tensor(x):
    return x.type().isSubtypeOf(torch._C.TensorType.get())
