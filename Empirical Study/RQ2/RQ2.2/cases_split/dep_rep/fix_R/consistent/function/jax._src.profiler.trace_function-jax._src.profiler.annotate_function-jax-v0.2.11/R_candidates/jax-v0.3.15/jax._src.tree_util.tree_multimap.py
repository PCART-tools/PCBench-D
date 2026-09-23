def tree_multimap(*args, **kwargs):
  """Deprecated alias of :func:`jax.tree_util.tree_map`"""
  warnings.warn('jax.tree_util.tree_multimap() is deprecated. Please use jax.tree_util.tree_map() '
                'instead as a drop-in replacement.', FutureWarning)
  return tree_map(*args, **kwargs)
