def _addupdate_abstract_eval(ref_aval: AbstractRef,
                             val_aval: core.AbstractValue,
                             *args: Any, tree):
  indexers = tree_util.tree_unflatten(tree, args)
  if not isinstance(ref_aval, AbstractRef):
    raise ValueError(f"`addupdate` must be called on `Ref` types: {ref_aval}.")
  if isinstance(ref_aval.inner_aval, core.ShapedArray):
    val_aval = core.raise_to_shaped(val_aval)
    slice_shape = _shape_after_indexing(ref_aval.shape, indexers)
    assert isinstance(val_aval, core.ShapedArray)
    if slice_shape != val_aval.shape:
      raise ValueError("Invalid shape for `addupdate`. "
                       f"Ref shape: {ref_aval.shape}. "
                       f"Slice shape: {slice_shape}. "
                       f"Value shape: {val_aval.shape}. "
                       f"Indices: {indexers}. ")
    if ref_aval.dtype != val_aval.dtype:
      raise ValueError("Invalid dtype for `addupdate`. "
                       f"Ref dtype: {ref_aval.dtype}. "
                       f"Value shape: {val_aval.dtype}. ")
  else:
    # Check that the indexers are valid
    if indexers:
      raise ValueError("Cannot index non-shaped array with nontrivial indices.")
  return [], {AccumEffect(0)}
