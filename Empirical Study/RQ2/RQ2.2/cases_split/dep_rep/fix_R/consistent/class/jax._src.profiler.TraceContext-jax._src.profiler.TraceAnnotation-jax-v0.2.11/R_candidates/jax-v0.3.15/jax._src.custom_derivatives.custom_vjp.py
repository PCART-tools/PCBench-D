@custom_api_util.register_custom_decorator_type
class custom_vjp(Generic[ReturnValue]):
  """Set up a JAX-transformable function for a custom VJP rule definition.

  This class is meant to be used as a function decorator. Instances are
  callables that behave similarly to the underlying function to which the
  decorator was applied, except when a reverse-mode differentiation
  transformation (like :py:func:`jax.grad`) is applied, in which case a custom
  user-supplied VJP rule function is used instead of tracing into and performing
  automatic differentiation of the underlying function's implementation. There
  is a single instance method, :py:func:`~jax.custom_vjp.defvjp`, which may be
  used to define the custom VJP rule.

  This decorator precludes the use of forward-mode automatic differentiation.

  For example::

    @jax.custom_vjp
    def f(x, y):
      return jnp.sin(x) * y

    def f_fwd(x, y):
      return f(x, y), (jnp.cos(x), jnp.sin(x), y)

    def f_bwd(res, g):
      cos_x, sin_x, y = res
      return (cos_x * g * y, sin_x * g)

    f.defvjp(f_fwd, f_bwd)

  For a more detailed introduction, see the tutorial_.

  .. _tutorial: https://jax.readthedocs.io/en/latest/notebooks/Custom_derivative_rules_for_Python_code.html
  """

  def __init__(self,
               fun: Callable[..., ReturnValue],
               nondiff_argnums: Tuple[int, ...] = ()):
    update_wrapper(self, fun)
    self.fun = fun
    self.nondiff_argnums = nondiff_argnums
    self.fwd: Optional[Callable[..., Tuple[ReturnValue, Any]]] = None
    self.bwd: Optional[Callable[..., Tuple[Any, ...]]] = None

  __getattr__ = custom_api_util.forward_attr

  def defvjp(self,
             fwd: Callable[..., Tuple[ReturnValue, Any]],
             bwd: Callable[..., Tuple[Any, ...]]) -> None:
    """Define a custom VJP rule for the function represented by this instance.

    Args:
      fwd: a Python callable representing the forward pass of the custom VJP
        rule. When there are no ``nondiff_argnums``, the ``fwd`` function has
        the same input signature as the underlying primal function. It should
        return as output a pair, where the first element represents the primal
        output and the second element represents any "residual" values to store
        from the forward pass for use on the backward pass by the function
        ``bwd``. Input arguments and elements of the output pair may be arrays
        or nested tuples/lists/dicts thereof.
      bwd: a Python callable representing the backward pass of the custom VJP
        rule. When there are no ``nondiff_argnums``, the ``bwd`` function takes
        two arguments, where the first is the "residual" values produced on the
        forward pass by ``fwd``, and the second is the output cotangent with the
        same structure as the primal function output. The output of ``bwd`` must
        be a tuple of length equal to the number of arguments of the primal
        function, and the tuple elements may be arrays or nested
        tuples/lists/dicts thereof so as to match the structure of the primal
        input arguments.

    Returns:
      None.

    Example::

      @jax.custom_vjp
      def f(x, y):
        return jnp.sin(x) * y

      def f_fwd(x, y):
        return f(x, y), (jnp.cos(x), jnp.sin(x), y)

      def f_bwd(res, g):
        cos_x, sin_x, y = res
        return (cos_x * g * y, sin_x * g)

      f.defvjp(f_fwd, f_bwd)
    """
    self.fwd = fwd
    self.bwd = bwd

  @traceback_util.api_boundary
  def __call__(self, *args: Any, **kwargs: Any) -> ReturnValue:  # pytype: disable=invalid-annotation
    if not self.fwd or not self.bwd:
      msg = "No VJP defined for custom_vjp function {} using defvjp."
      raise AttributeError(msg.format(self.__name__))
    args = _resolve_kwargs(self.fun, args, kwargs)
    if config.jax_enable_custom_vjp_by_custom_transpose:
      if self.nondiff_argnums:
        raise NotImplementedError(
            'nondiff_argnums not implemented for new custom_vjp')
      return custom_vjp_by_custom_transpose(self.fun, self.fwd, self.bwd)(*args)
    else:
      if self.nondiff_argnums:
        for i in self.nondiff_argnums: _check_for_tracers(args[i])
        nondiff_argnums = set(self.nondiff_argnums)
        dyn_argnums = [i for i in range(len(args)) if i not in nondiff_argnums]
        f_, dyn_args = argnums_partial(lu.wrap_init(self.fun), dyn_argnums,
                                       args, require_static_args_hashable=False)
        static_args = [args[i] for i in self.nondiff_argnums]
        fwd, _ = argnums_partial(lu.wrap_init(self.fwd), dyn_argnums, args,
                                 require_static_args_hashable=False)
        bwd = _add_args(lu.wrap_init(self.bwd), static_args)
      else:
        f_, dyn_args = lu.wrap_init(self.fun), args
        fwd, bwd = lu.wrap_init(self.fwd), lu.wrap_init(self.bwd)
      args_flat, in_tree = tree_flatten(dyn_args)
      in_avals = [core.raise_to_shaped(core.get_aval(x)) for x in args_flat]
      flat_fun, out_tree = flatten_fun_nokwargs(f_, in_tree)
      flat_fwd, out_trees = _flatten_fwd(fwd, in_tree)
      flat_bwd = _flatten_bwd(bwd, in_tree, in_avals, out_trees)
      out_flat = custom_vjp_call_p.bind(flat_fun, flat_fwd, flat_bwd,
                                        *args_flat, out_trees=out_trees)
      fst, aux = lu.merge_linear_aux(out_tree, out_trees)
      out_tree = aux if fst else aux[0]
      return tree_unflatten(out_tree, out_flat)
