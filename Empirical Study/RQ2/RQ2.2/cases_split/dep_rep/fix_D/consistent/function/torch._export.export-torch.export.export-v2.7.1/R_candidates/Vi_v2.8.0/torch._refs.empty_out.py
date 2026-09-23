@aten.empty.out.py_impl(DispatchKey.CompositeImplicitAutograd)
def empty_out(
    size: TensorLikeType,
    out: TensorLikeType,
    memory_format: Optional[torch.memory_format] = None,
) -> TensorLikeType:
    return out
