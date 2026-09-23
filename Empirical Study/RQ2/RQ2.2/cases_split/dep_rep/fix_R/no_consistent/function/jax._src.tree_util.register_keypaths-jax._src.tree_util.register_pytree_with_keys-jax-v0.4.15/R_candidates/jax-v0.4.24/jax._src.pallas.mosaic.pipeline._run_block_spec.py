def _run_block_spec(
    block_spec: core.BlockSpec, indices: GridIndices
) -> tuple[Union[slice, indexing.Slice], ...]:
  """Runs a block spec for the given indices and returns the slices.

  Args:
    block_spec: Block spec to run.
    indices: Grid indices to run on.

  Returns:
    Array slices for the block spec.
  """
  index_map = block_spec.index_map
  if index_map is None:
    raise ValueError("Block spec index_map is None.")
  block_indices = index_map(*indices)
  return tuple(
      indexing.ds(
          primitives.multiple_of(index * block_size, block_size), block_size
      )
      for index, block_size in zip(
          block_indices, cast(Any, block_spec.block_shape)
      )
  )
