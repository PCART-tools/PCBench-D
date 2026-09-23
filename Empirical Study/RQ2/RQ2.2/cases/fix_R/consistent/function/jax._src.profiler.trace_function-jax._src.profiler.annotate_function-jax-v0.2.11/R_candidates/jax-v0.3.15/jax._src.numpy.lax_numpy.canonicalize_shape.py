def canonicalize_shape(
    shape: Union[core.Shape, int, core.Tracer], context: str="") -> core.Shape:
  if isinstance(shape, core.Tracer) or ndim(shape) == 0:
    return core.canonicalize_shape((shape,), context)
  else:
    return core.canonicalize_shape(shape, context)  # type: ignore
