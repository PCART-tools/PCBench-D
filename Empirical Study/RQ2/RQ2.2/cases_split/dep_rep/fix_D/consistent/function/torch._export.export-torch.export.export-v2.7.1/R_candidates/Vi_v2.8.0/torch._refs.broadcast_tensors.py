@aten.broadcast_tensors.default.py_impl(DispatchKey.CompositeImplicitAutograd)
@aten.broadcast_tensors.default.py_impl(DispatchKey.Meta)
def broadcast_tensors(*tensors) -> list[TensorLikeType]:
    if len(tensors) == 1 and not isinstance(tensors[0], Tensor):
        tensors = tensors[0]
    return list(_maybe_broadcast(*tensors, preserve_cpu_scalar_tensors=False))
