def _iota_abstract_eval(*, dtype, shape, dimension):
  _check_shapelike("iota", "shape", shape)
  if not any(dtypes.issubdtype(dtype, t) for t in _num):
    msg = 'iota does not accept dtype {}. Accepted dtypes are subtypes of {}.'
    typename = str(np.dtype(dtype).name)
    accepted_typenames = (t.__name__ for t in _num)
    raise TypeError(msg.format(typename, ', '.join(accepted_typenames)))
  if not 0 <= dimension < len(shape):
    raise ValueError("iota dimension must be between 0 and len(shape), got "
                     f"dimension={dimension} for shape {shape}")
  if not any(isinstance(d, core.BInt) for d in shape):
    return ShapedArray(shape, dtype)
  # TODO(mattjj): unify DShapedArray with ShapedArray, and remove this code
  return core.DShapedArray(shape, dtype, False)
