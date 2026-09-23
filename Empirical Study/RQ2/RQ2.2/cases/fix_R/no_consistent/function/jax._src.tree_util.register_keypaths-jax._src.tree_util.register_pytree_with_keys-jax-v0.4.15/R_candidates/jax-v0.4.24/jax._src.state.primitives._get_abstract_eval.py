def _get_abstract_eval(ref_aval: AbstractRef, *args,
                       tree):
  indexers = tree_util.tree_unflatten(tree, args)
  if not isinstance(ref_aval, AbstractRef):
    raise ValueError(f"`get` must be called on `Ref` types: {ref_aval}.")
  if isinstance(ref_aval.inner_aval, core.ShapedArray):
    out_shape = _shape_after_indexing(ref_aval.shape, indexers)
    out_aval = ref_aval.inner_aval.update(shape=out_shape)
  else:
    if indexers:
      raise ValueError("Cannot index non-shaped array with nontrivial indices.")
    out_aval = ref_aval.inner_aval
  return (out_aval, {ReadEffect(0)})
