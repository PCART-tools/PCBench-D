  def __call__(self, *flat_args: jax.Array) -> Sequence[jax.Array]:
    args, kwargs = tree_util.tree_unflatten(self.in_tree, flat_args)
    return tree_util.tree_leaves(self.callback_func(*args, **kwargs))
