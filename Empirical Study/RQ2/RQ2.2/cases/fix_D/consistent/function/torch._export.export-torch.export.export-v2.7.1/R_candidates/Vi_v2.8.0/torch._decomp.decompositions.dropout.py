@register_decomposition(aten.dropout)
@aten.dropout.default.py_impl(DispatchKey.CompositeImplicitAutograd)
@aten.dropout.default.py_impl(DispatchKey.Autograd)
def dropout(input: Tensor, p: float, train: Optional[bool]):
    if train and p != 0:
        return aten.native_dropout(input, p, train)[0]
    else:
        return input.clone()
