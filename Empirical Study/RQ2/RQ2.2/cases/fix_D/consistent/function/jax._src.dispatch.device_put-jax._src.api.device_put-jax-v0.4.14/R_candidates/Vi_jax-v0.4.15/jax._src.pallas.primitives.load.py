def load(x_ref, idx, *, mask=None, other=None, cache_modifier="",
         eviction_policy="", volatile=False):
  idx = NDIndexer.from_indices_shape(idx, x_ref.shape)
  args = (idx,)
  if mask is not None:
    args = (*args, mask)
  if other is not None:
    assert mask is not None
    args = (*args, other)
  flat_args, args_tree = tree_util.tree_flatten(args)
  return load_p.bind(x_ref, *flat_args, masked=mask is not None, cache_modifier=cache_modifier,
                     eviction_policy=eviction_policy, is_volatile=volatile,
                     args_tree=args_tree)
