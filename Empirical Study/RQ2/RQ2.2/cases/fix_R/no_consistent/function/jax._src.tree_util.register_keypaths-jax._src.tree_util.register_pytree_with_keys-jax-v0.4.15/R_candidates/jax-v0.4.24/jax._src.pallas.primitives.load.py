def load(x_ref_or_view, idx, *, mask=None, other=None, cache_modifier=None,
         eviction_policy=None, volatile=False) -> jax.Array:
  x_ref, indexers = sp.get_ref_and_indexers(x_ref_or_view, idx, "load")
  args_flat, args_tree = tree_util.tree_flatten((x_ref, indexers, mask, other))
  return load_p.bind(
      *args_flat,
      args_tree=args_tree,
      cache_modifier=cache_modifier,
      eviction_policy=eviction_policy,
      is_volatile=volatile,
  )
