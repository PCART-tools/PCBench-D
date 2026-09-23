def _dma_slice_not_equal(
    dma_slice_a: tuple[Union[slice, indexing.Slice], ...],
    dma_slice_b: tuple[Union[slice, indexing.Slice], ...],
) -> jax.Array:
  """Returns True if the two slices are not equal."""
  dma_slice_not_equal = cast(jax.Array, False)
  for a, b in zip(dma_slice_a, dma_slice_b):
    dma_slice_not_equal = jnp.logical_or(
        dma_slice_not_equal, a.start != b.start
    )
  return dma_slice_not_equal
