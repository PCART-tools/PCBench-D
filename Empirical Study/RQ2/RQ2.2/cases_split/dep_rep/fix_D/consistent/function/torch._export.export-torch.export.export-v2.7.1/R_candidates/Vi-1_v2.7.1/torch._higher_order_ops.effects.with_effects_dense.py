@with_effects.py_impl(DispatchKey.CompositeExplicitAutograd)
def with_effects_dense(
    token: torch.Tensor,
    op: torch._ops.OpOverload,
    *args: tuple[Any, ...],
    **kwargs: dict[str, Any],
) -> tuple[torch.Tensor, ...]:
    out = op(*args, **kwargs)
    new_token = new_token_tensor()
    if isinstance(out, tuple):
        return (new_token, *out)
    return (new_token, out)
