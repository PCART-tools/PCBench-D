def _tile_ref(ref: state.AbstractRef, block_shape: tuple[int, ...] | None
             ) -> state.AbstractRef:
  if block_shape is None:
    return ref
  shape = tuple(s for s in block_shape if s is not None)
  return ref.update(inner_aval=ref.inner_aval.update(shape=shape))
