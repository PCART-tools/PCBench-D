def _load_abstract_eval(ref_aval, *all_avals, args_tree,
                        **params: Any):
  idx_aval, *_ = tree_util.tree_unflatten(args_tree, all_avals)
  return (jax_core.ShapedArray(idx_aval.get_indexer_shape(), ref_aval.dtype),
          {state.ReadEffect(0)})
