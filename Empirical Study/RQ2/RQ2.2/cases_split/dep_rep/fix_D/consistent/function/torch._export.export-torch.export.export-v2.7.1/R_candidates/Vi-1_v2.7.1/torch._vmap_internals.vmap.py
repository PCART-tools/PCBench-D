@deprecated(
    "Please use `torch.vmap` instead of `torch._vmap_internals.vmap`.",
    category=FutureWarning,
)
def vmap(func: Callable, in_dims: in_dims_t = 0, out_dims: out_dims_t = 0) -> Callable:
    """
    Please use torch.vmap instead of this API.
    """
    return _vmap(func, in_dims, out_dims)
