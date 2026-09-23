def shaped_array_ref(shape: tuple[int, ...], dtype,
                     weak_type: bool = False,
                     named_shape = None) -> AbstractRef[core.AbstractValue]:
  return AbstractRef(core.ShapedArray(shape, dtype, weak_type=weak_type,
                                      named_shape=named_shape))
