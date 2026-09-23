def _iota_abstract_eval(*dyn_shape, dtype, shape, dimension):
  if not dyn_shape:
    # TODO(mattjj) Generalize shape_like checking to permit dynamic shapes
    _check_shapelike("iota", "shape", shape)
  if not any(dtypes.issubdtype(dtype, t) for t in _num):
    msg = 'iota does not accept dtype {}. Accepted dtypes are subtypes of {}.'
    typename = dtype_to_string(dtype)
    accepted_typenames = (t.__name__ for t in _num)
    raise TypeError(msg.format(typename, ', '.join(accepted_typenames)))
  if not 0 <= dimension < len(shape):
    raise ValueError("iota dimension must be between 0 and len(shape), got "
                     f"{dimension=} for {shape=}")
  if (not dyn_shape and
      not any(isinstance(d, core.DArray) and
              type(core.get_aval(d).dtype) is core.bint for d in shape)):
    return ShapedArray(shape, dtype)
  # TODO(mattjj): unify DShapedArray with ShapedArray, and remove this code
  return core.DShapedArray(_merge_dyn_shape(shape, dyn_shape), dtype, False)
