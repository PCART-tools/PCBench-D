def _make_abstract_python_scalar(typ, val):
  # Note: all python scalar types are weak except bool, because bool only
  # comes in a single width.
  return ShapedArray((), dtypes._scalar_type_to_dtype(typ, val),
                     weak_type=typ is not bool)
