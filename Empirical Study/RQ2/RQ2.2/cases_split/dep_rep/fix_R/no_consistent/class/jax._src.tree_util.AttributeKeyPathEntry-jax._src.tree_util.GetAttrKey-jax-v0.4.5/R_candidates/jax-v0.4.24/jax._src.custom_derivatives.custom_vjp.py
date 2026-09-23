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
               nondiff_argnums: tuple[int, ...] = ()):
    update_wrapper(self, fun)
    self.fun = fun
    self.nondiff_argnums = nondiff_argnums
    self.fwd: Callable[..., tuple[ReturnValue, Any]] | None = None
    self.bwd: Callable[..., tuple[Any, ...]] | None = None
    self.symbolic_zeros = False

  __getattr__ = custom_api_util.forward_attr

  def defvjp(self,
             fwd: Callable[..., tuple[ReturnValue, Any]],
             bwd: Callable[..., tuple[Any, ...]],
             symbolic_zeros: bool = False,
             ) -> None:
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
      symbolic_zeros: boolean, determining whether to indicate symbolic zeros
        to the ``fwd`` and ``bwd`` rules. Enabling this option allows custom
        derivative rules to detect when certain inputs, and when certain
        output cotangents, are not involved in differentiation. If ``True``:

        * ``fwd`` must accept, in place of each leaf value ``x`` in
          the pytree comprising an argument to the original function,
          an object (of type
          ``jax.custom_derivatives.CustomVJPPrimal``) with two
          attributes instead: ``value`` and ``perturbed``. The
          ``value`` field is the original primal argument, and
          ``perturbed`` is a boolean.  The ``perturbed`` bit indicates
          whether the argument is involved in differentiation (i.e.,
          if it is ``False``, then the corresponding Jacobian "column"
          is zero).

        * ``bwd`` will be passed objects representing static symbolic zeros in
          its cotangent argument in correspondence with unperturbed values;
          otherwise, only standard JAX types (e.g. array-likes) are passed.

        Setting this option to ``True`` allows these rules to detect whether
        certain inputs and outputs are not involved in differentiation, but at
        the cost of special handling. For instance:

        * The signature of ``fwd`` changes, and the objects it is passed cannot
          be output from the rule directly.

        * The ``bwd`` rule is passed objects that are not entirely array-like,
          and that cannot be passed to most ``jax.numpy`` functions.

        * Any custom pytree nodes involved in the primal function's arguments
          must accept, in their unflattening functions, the two-field record
          objects that are given as input leaves to the ``fwd`` rule.

        Default ``False``.

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
    self.symbolic_zeros = symbolic_zeros

  @traceback_util.api_boundary
  def __call__(self, *args: Any, **kwargs: Any) -> ReturnValue:  # pytype: disable=invalid-annotation
    primal_name = getattr(self.fun, '__name__', str(self.fun))
    if not self.fwd or not self.bwd:
      msg = f"No VJP defined for custom_vjp function {primal_name} using defvjp."
      raise AttributeError(msg)
    fwd_name = getattr(self.fwd, '__name__', str(self.fwd))
    args = _resolve_kwargs(self.fun, args, kwargs)
    if config.enable_custom_vjp_by_custom_transpose.value:
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
      flat_fun, out_type = _flatten_fun_nokwargs(f_, in_tree)
      flat_fwd, out_trees = _flatten_fwd(fwd, self.symbolic_zeros, primal_name,
                                         fwd_name, in_tree, out_type)
      flat_bwd = _flatten_bwd(bwd, in_tree, in_avals, out_trees).call_wrapped
      out_flat = custom_vjp_call_p.bind(flat_fun, flat_fwd, flat_bwd,
                                        *args_flat, out_trees=out_trees,
                                        symbolic_zeros=self.symbolic_zeros)
      _, (out_tree, _) = lu.merge_linear_aux(out_type, out_trees)
      return tree_unflatten(out_tree, out_flat)
