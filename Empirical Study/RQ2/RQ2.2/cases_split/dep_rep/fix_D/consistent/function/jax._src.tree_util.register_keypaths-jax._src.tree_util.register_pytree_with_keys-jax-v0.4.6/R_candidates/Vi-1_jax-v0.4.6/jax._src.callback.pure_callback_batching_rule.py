def pure_callback_batching_rule(args, dims, *, callback, vectorized: bool,
                                result_avals: Sequence[core.ShapedArray]):
  axis_size = next(a.shape[0] for a, d in zip(args, dims)
                   if d is not batching.not_mapped)
  new_args = [arg if dim is batching.not_mapped else
              batching.moveaxis(arg, dim, 0) for arg, dim in zip(args, dims)]
  if vectorized:
    result_avals = tuple(
        core.unmapped_aval(axis_size, core.no_axis_name, 0, aval)  # type: ignore
        for aval in result_avals)
    outvals = pure_callback_p.bind(
        *new_args, callback=callback, vectorized=vectorized,
        result_avals=result_avals)
  else:
    is_batched = [d is not batching.not_mapped for d in dims]
    unbatched_args, batched_args = util.partition_list(is_batched, new_args)
    def _batch_fun(batched_args):
      merged_args = util.merge_lists(is_batched, unbatched_args, batched_args)
      return pure_callback_p.bind(
          *merged_args, callback=callback, result_avals=result_avals,
          vectorized=vectorized)
    from jax._src.lax.control_flow import map as lax_map
    outvals = lax_map(_batch_fun, batched_args)
  return tuple(outvals), (0,) * len(outvals)
