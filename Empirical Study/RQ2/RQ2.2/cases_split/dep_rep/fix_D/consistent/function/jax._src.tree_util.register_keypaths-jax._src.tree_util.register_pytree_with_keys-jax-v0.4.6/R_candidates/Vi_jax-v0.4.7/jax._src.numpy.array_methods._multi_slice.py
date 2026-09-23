@core.stash_axis_env()
@partial(jax.jit, static_argnums=(1,2,3))
def _multi_slice(arr: ArrayLike,
                 start_indices: Tuple[Tuple[int, ...]],
                 limit_indices: Tuple[Tuple[int, ...]],
                 removed_dims: Tuple[Tuple[int, ...]]) -> List[Array]:
  """Extracts multiple slices from `arr`.

  This is used to shard DeviceArray arguments to pmap. It's implemented as a
  DeviceArray method here to avoid circular imports.
  """
  results: List[Array] = []
  for starts, limits, removed in safe_zip(start_indices, limit_indices, removed_dims):
    sliced = lax.slice(arr, starts, limits)
    if removed:
      sliced = lax.squeeze(sliced, removed)
    results.append(sliced)
  return results
