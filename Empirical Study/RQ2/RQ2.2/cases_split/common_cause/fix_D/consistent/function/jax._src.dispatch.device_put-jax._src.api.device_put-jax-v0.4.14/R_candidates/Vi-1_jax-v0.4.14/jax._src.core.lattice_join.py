def lattice_join(x: AbstractValue | None,
                 y: AbstractValue | None) -> AbstractValue:
  if x is None:
    return cast(AbstractValue, y)
  elif y is None:
    return cast(AbstractValue, x)
  elif isinstance(x, type(y)):
    return y.join(x)
  elif isinstance(y, type(x)):
    return x.join(y)
  elif isinstance(x, DShapedArray) and isinstance(y, ShapedArray):
    # TODO(mattjj): remove this special case after dynamic shapes are integrated
    return x.join(y)
  else:
    raise TypeError(x, y)
