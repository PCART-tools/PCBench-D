def debug_callback(callback: Callable[..., Any], effect: DebugEffect, *args,
                   **kwargs):
  """Calls a stageable Python callback.

  `debug_callback` enables you to pass in a Python function that can be called
  inside of a staged JAX program. A `debug_callback` follows existing JAX
  transformation *pure* operational semantics, which are therefore unaware of
  side-effects. This means the effect could be dropped, duplicated, or
  potentially reordered in the presence of higher-order primitives and
  transformations.

  We want this behavior because we'd like `debug_callback` to be "innocuous",
  i.e. we want these primitives to change the JAX computation as little as
  possible while revealing as much about them as possible, such as which parts
  of the computation are duplicated or dropped.

  Args:
    callback: A Python callable.
    effect: A `DebugEffect`.
    *args: The positional arguments to the callback.
    **kwargs: The positional arguments to the callback.
  Returns:
    The value of `callback(*args, **kwargs)`.
  """
  if not isinstance(effect, DebugEffect):
    raise ValueError("Can only use `DebugEffect` effects in `debug_callback`")
  flat_args, in_tree = tree_util.tree_flatten((args, kwargs))
  return debug_callback_p.bind(*flat_args, callback=callback, effect=effect,
                               in_tree=in_tree)
