def _swap_abstract_eval(ref_aval: AbstractRef,
                        val_aval: core.AbstractValue,
                        *args: Any, tree):
  indexers = tree_util.tree_unflatten(tree, args)
  out_aval: core.AbstractValue
  if not isinstance(ref_aval, AbstractRef):
    raise ValueError(f"`swap` must be called on `Ref` types: {ref_aval}.")
  if isinstance(ref_aval.inner_aval, core.ShapedArray):
    val_aval = core.raise_to_shaped(val_aval)
    assert isinstance(val_aval, core.ShapedArray)
    expected_out_shape = _shape_after_indexing(ref_aval.shape, indexers)
    if expected_out_shape != val_aval.shape:
      raise ValueError("Invalid shape for `swap`. "
                       f"Ref shape: {ref_aval.shape}. "
                       f"Expected shape: {expected_out_shape}. "
                       f"Value shape: {val_aval.shape}. "
                       f"Indices: {indexers}. ")
    if ref_aval.dtype != val_aval.dtype:
      raise ValueError("Invalid dtype for `swap`. "
                       f"Ref dtype: {ref_aval.dtype}. "
                       f"Value shape: {val_aval.dtype}. ")
    out_aval = core.ShapedArray(expected_out_shape, ref_aval.dtype)
  else:
    if indexers:
      raise ValueError("Cannot index non-shaped array with nontrivial indices.")
    out_aval = ref_aval.inner_aval
  return (out_aval, {WriteEffect(0)})
