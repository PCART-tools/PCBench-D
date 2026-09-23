def _get_abstract_eval(ref_aval: AbstractRef, *idx,
                       indexed_dims):
  if not isinstance(ref_aval, AbstractRef):
    raise ValueError(f"`get` must be called on `Ref` types: {ref_aval}.")
  if isinstance(ref_aval.inner_aval, core.ShapedArray):
    if not isinstance(ref_aval.inner_aval, core.ShapedArray):
      raise ValueError("`get` with nontrivial indexing must be called "
                       f"on `ShapedArray` `Ref`: {ref_aval}.")
    if len(indexed_dims) != len(ref_aval.shape):
      raise ValueError("`indexed_dims` must be the same length as `Ref` shape.")
    if sum(indexed_dims) != len(idx):
      raise ValueError(f"Invalid `idx` and `indexed_dims`: {idx}, {indexed_dims}")
    idx_shapes = tuple(i.shape for i in idx)
    shape = _get_slice_output_shape(ref_aval.shape, idx_shapes, indexed_dims)
    out_aval = ref_aval.inner_aval.update(shape=shape)
  else:
    if idx:
      raise ValueError("Cannot index non-shaped array with nontrivial indices.")
    out_aval = ref_aval.inner_aval
  return (out_aval, {ReadEffect(0)})
