@_unsafe_set_version_counter.py_impl(FunctionalTensorMode)
def _unsafe_set_version_counter_functional(ctx, tensors, versions):
    torch._C._autograd._unsafe_set_version_counter(tensors, versions)
