def named_call(
    fun: Callable[..., Any],
    *,
    name: Optional[str] = None,
  ) -> Callable[..., Any]:
  """Adds a user specified name to a function when staging out JAX computations.

  When staging out computations for just-in-time compilation to XLA (or other
  backends such as TensorFlow) JAX runs your Python program but by default does
  not preserve any of the function names or other metadata associated with it.
  This can make debugging the staged out (and/or compiled) representation of
  your program complicated because there is limited context information for each
  operation being executed.

  `named_call` tells JAX to stage the given function out as a subcomputation
  with a specific name. When the staged out program is compiled with XLA these
  named subcomputations are preserved and show up in debugging utilities like
  the TensorFlow Profiler in TensorBoard. Names are also preserved when staging
  out JAX programs to TensorFlow using :func:`experimental.jax2tf.convert`.

  Args:
    fun: Function to be wrapped. This can be any Callable.
    name: Optional. The prefix to use to name all sub computations created
      within the name scope. Use the fun.__name__ if not specified.

  Returns:
    A version of `fun` that is wrapped in a name_scope.
  """
  if name is None:
    name = fun.__name__

  _, in_tree = tree_flatten(())

  if config.jax_experimental_name_stack:
    return source_info_util.extend_name_stack(name)(fun)

  @functools.wraps(fun)
  def named_call_f(*args, **kwargs):
    lu_f = lu.wrap_init(lambda: fun(*args, **kwargs))
    flat_f, out_tree = flatten_fun_nokwargs(lu_f, in_tree)
    out_flat = core.named_call_p.bind(flat_f, name=name)
    return tree_unflatten(out_tree(), out_flat)

  return named_call_f
