def physical_aval(aval):
  aval_dtype = getattr(aval, 'dtype', None)
  if aval_dtype and dtypes.issubdtype(aval_dtype, dtypes.extended):
    ctor = type(aval)
    aval_shape = getattr(aval, 'shape', None)
    assert aval_shape is not None, (ctor, aval)
    elt_aval = aval_dtype._rules.physical_element_aval(aval_dtype)
    assert type(elt_aval) is ShapedArray
    return ctor((*aval_shape, *elt_aval.shape), elt_aval.dtype)  # pytype: disable=wrong-arg-count
  else:
    return aval
