def _is_bint_axis_size(d: int | core.DArray | core.Var) -> bool:
  if isinstance(d, core.DArray):
    assert not d.shape                 # pytype: disable=attribute-error
    return type(d.dtype) is core.bint  # pytype: disable=attribute-error
  elif isinstance(d, core.Var):
    return (isinstance(d.aval, core.DShapedArray) and  # pytype: disable=attribute-error
            type(d.aval.dtype) is core.bint)           # pytype: disable=attribute-error
  return False
