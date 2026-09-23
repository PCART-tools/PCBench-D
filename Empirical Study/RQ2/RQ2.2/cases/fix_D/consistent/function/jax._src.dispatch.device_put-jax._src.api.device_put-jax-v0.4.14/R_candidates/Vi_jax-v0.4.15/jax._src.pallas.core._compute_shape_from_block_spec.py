def _compute_shape_from_block_spec(block_spec: BlockSpec | None,
                                   arg_shape: tuple[int, ...]
                                   ) -> tuple[int, ...]:
  if block_spec is _no_block_spec:
    return arg_shape
  return tuple(s for s in block_spec.block_shape if s is not None)
