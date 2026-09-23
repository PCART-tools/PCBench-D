def canonicalize_shape(shape: Any, context: str="") -> core.Shape:
  if (not isinstance(shape, (tuple, list)) and
      (getattr(shape, 'ndim', None) == 0 or ndim(shape) == 0)):
    return core.canonicalize_shape((shape,), context)  # type: ignore
  else:
    return core.canonicalize_shape(shape, context)  # type: ignore
