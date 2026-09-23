def _tree_map_with_kwargs(f, *args, **kwargs):
  """jax.tree_util.tree_map that supports kwargs."""
  kwargs_keys = kwargs.keys()
  kwargs_values = kwargs.values()
  return tree_util.tree_map(
      lambda arg0, partial_f, *args: partial_f(arg0, *args),
      args[0],
      tree_util.tree_map(
          lambda _, *tree_mapped_kwargs_values: partial(
              f, **dict(zip(kwargs_keys, tree_mapped_kwargs_values))
          ),
          args[0],
          *kwargs_values,
          is_leaf=lambda x: x is None,
      ),
      *args[1:],
  )
