def _unwrap_batched(
        batched_outputs: Union[Tensor, Tuple[Tensor, ...]],
        out_dims: out_dims_t,
        vmap_level: int, batch_size: int, func: Callable) -> Tuple:
    num_outputs = _num_outputs(batched_outputs)
    out_dims_as_tuple = _as_tuple(
        out_dims, num_outputs,
        lambda: f'vmap({_get_name(func)}, ..., out_dims={out_dims}): `out_dims` must '
                f'have one dim per output (got {num_outputs} outputs) of {_get_name(func)}.')

    # NOTE [Ignored _remove_batch_dim, _add_batch_dim]
    # There is something wrong with our type bindings for functions that begin
    # with '_', see #40397.
    if isinstance(batched_outputs, Tensor):
        out_dim = out_dims_as_tuple[0]
        return torch._remove_batch_dim(batched_outputs, vmap_level, batch_size, out_dim)  # type: ignore[return-value]
    return tuple(torch._remove_batch_dim(out, vmap_level, batch_size, out_dim)
                 for out, out_dim in zip(batched_outputs, out_dims_as_tuple))
