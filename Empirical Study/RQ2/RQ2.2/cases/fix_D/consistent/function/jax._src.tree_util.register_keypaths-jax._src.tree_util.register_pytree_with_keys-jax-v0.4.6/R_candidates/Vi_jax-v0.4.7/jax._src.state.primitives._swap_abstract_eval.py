def _swap_abstract_eval(ref_aval: AbstractRef,
                        val_aval: core.AbstractValue,
                        *idx: core.ShapedArray, indexed_dims: Tuple[bool]):
  out_aval: core.AbstractValue
  if not isinstance(ref_aval, AbstractRef):
    raise ValueError(f"`swap` must be called on `Ref` types: {ref_aval}.")
  if isinstance(ref_aval.inner_aval, core.ShapedArray):
    if len(indexed_dims) != len(ref_aval.shape):
      raise ValueError("`indexed_dims` must be the same length as `Ref` shape.")
    if sum(indexed_dims) != len(idx):
      raise ValueError(f"Invalid `idx` and `indexed_dims`: {idx}, {indexed_dims}")
    val_aval = core.raise_to_shaped(val_aval)
    assert isinstance(val_aval, core.ShapedArray)
    idx_shapes = tuple(i.shape for i in idx)
    expected_output_shape = _get_slice_output_shape(
        ref_aval.shape, idx_shapes, indexed_dims)
    if expected_output_shape != val_aval.shape:
      raise ValueError("Invalid shape for `swap`. "
                       f"Ref shape: {ref_aval.shape}. "
                       f"Value shape: {val_aval.shape}. "
                       f"Indices: {idx}. ")
    if ref_aval.dtype != val_aval.dtype:
      raise ValueError("Invalid dtype for `swap`. "
                       f"Ref dtype: {ref_aval.dtype}. "
                       f"Value shape: {val_aval.dtype}. ")
    out_aval = core.ShapedArray(expected_output_shape, ref_aval.dtype)
  else:
    if idx:
      raise ValueError("`swap` with nontrivial indexing must be called "
                       f"on `ShapedArray` `Ref`: {ref_aval}.")
    out_aval = ref_aval.inner_aval
  return (out_aval, {WriteEffect(0)})
