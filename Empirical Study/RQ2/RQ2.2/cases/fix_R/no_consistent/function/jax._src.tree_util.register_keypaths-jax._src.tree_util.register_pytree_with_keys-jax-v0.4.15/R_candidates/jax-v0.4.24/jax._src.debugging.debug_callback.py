def debug_callback(callback: Callable[..., Any], *args: Any,
                   ordered: bool = False, **kwargs: Any) -> None:
  """Calls a stageable Python callback.

  For more explanation, see `External Callbacks`_.

  ``jax.debug.callback`` enables you to pass in a Python function that can be called
  inside of a staged JAX program. A ``jax.debug.callback`` follows existing JAX
  transformation *pure* operational semantics, which are therefore unaware of
  side-effects. This means the effect could be dropped, duplicated, or
  potentially reordered in the presence of higher-order primitives and
  transformations.

  We want this behavior because we'd like ``jax.debug.callback`` to be "innocuous",
  i.e. we want these primitives to change the JAX computation as little as
  possible while revealing as much about them as possible, such as which parts
  of the computation are duplicated or dropped.

  Args:
    callback: A Python callable. Its return value will be ignored.
    *args: The positional arguments to the callback.
    ordered: A keyword only argument used to indicate whether or not the
      staged out computation will enforce ordering of this callback w.r.t.
      other ordered callbacks.
    **kwargs: The keyword arguments to the callback.

  Returns:
    None

  See Also:
    - :func:`jax.experimental.io_callback`: callback designed for impure functions.
    - :func:`jax.pure_callback`: callback designed for pure functions.
    - :func:`jax.debug.print`: callback designed for printing.

  .. _External Callbacks: https://jax.readthedocs.io/en/latest/notebooks/external_callbacks.html
  """
  if not callable(callback):
    raise TypeError("first argument to jax.debug.callback must be callable, "
                    f"but got an object of type {type(callback)}")
  flat_args, in_tree = tree_util.tree_flatten((args, kwargs))
  effect = ordered_debug_effect if ordered else debug_effect
  def _flat_callback(*flat_args):
    args, kwargs = tree_util.tree_unflatten(in_tree, flat_args)
    callback(*args, **kwargs)
    return []
  debug_callback_p.bind(*flat_args, callback=_flat_callback, effect=effect)
