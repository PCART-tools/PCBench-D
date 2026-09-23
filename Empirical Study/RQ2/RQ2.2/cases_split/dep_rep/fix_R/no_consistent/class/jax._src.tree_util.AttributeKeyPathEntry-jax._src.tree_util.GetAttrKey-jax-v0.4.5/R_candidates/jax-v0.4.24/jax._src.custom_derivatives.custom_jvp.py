@custom_api_util.register_custom_decorator_type
class custom_jvp(Generic[ReturnValue]):
  """Set up a JAX-transformable function for a custom JVP rule definition.

  This class is meant to be used as a function decorator. Instances are
  callables that behave similarly to the underlying function to which the
  decorator was applied, except when a differentiation transformation (like
  :py:func:`jax.jvp` or :py:func:`jax.grad`) is applied, in which case a custom
  user-supplied JVP rule function is used instead of tracing into and
  performing automatic differentiation of the underlying function's
  implementation.

  There are two instance methods available for defining the custom JVP rule:
  :py:func:`~jax.custom_jvp.defjvp` for defining a *single* custom JVP rule for
  all the function's inputs, and for convenience
  :py:func:`~jax.custom_jvp.defjvps`, which wraps
  :py:func:`~jax.custom_jvp.defjvp`, and allows you to provide separate
  definitions for the partial derivatives of the function w.r.t. each of its
  arguments.

  For example::

    @jax.custom_jvp
    def f(x, y):
      return jnp.sin(x) * y

    @f.defjvp
    def f_jvp(primals, tangents):
      x, y = primals
      x_dot, y_dot = tangents
      primal_out = f(x, y)
      tangent_out = jnp.cos(x) * x_dot * y + jnp.sin(x) * y_dot
      return primal_out, tangent_out

  For a more detailed introduction, see the tutorial_.

  .. _tutorial: https://jax.readthedocs.io/en/latest/notebooks/Custom_derivative_rules_for_Python_code.html
  """
  fun: Callable[..., ReturnValue]
  nondiff_argnums: tuple[int, ...]
  jvp: Callable[..., tuple[ReturnValue, ReturnValue]] | None = None
  symbolic_zeros: bool = False

  def __init__(self,
               fun: Callable[..., ReturnValue],
               nondiff_argnums: tuple[int, ...] = (),
               ):
    update_wrapper(self, fun)
    self.fun = fun
    self.nondiff_argnums = nondiff_argnums

  __getattr__ = custom_api_util.forward_attr

  def defjvp(self,
             jvp: Callable[..., tuple[ReturnValue, ReturnValue]],
             symbolic_zeros: bool = False,
             ) -> Callable[..., tuple[ReturnValue, ReturnValue]]:
    """Define a custom JVP rule for the function represented by this instance.

    Args:
      jvp: a Python callable representing the custom JVP rule. When there are no
        ``nondiff_argnums``, the ``jvp`` function should accept two arguments,
        where the first is a tuple of primal inputs and the second is a tuple of
        tangent inputs. The lengths of both tuples are equal to the number of
        parameters of the ``custom_jvp`` function. The ``jvp`` function should
        produce as output a pair where the first element is the primal output
        and the second element is the tangent output. Elements of the input and
        output tuples may be arrays or any nested tuples/lists/dicts thereof.
      symbolic_zeros: boolean, indicating whether the rule should be passed
        objects representing static symbolic zeros in its tangent argument in
        correspondence with unperturbed values; otherwise, only standard JAX
        types (e.g. array-likes) are passed. Setting this option to ``True``
        allows a JVP rule to detect whether certain inputs are not involved in
        differentiation, but at the cost of needing special handling for these
        objects (which e.g. can't be passed into jax.numpy functions). Default
        ``False``.

    Returns:
      None.

    Example::

      @jax.custom_jvp
      def f(x, y):
        return jnp.sin(x) * y

      @f.defjvp
      def f_jvp(primals, tangents):
        x, y = primals
        x_dot, y_dot = tangents
        primal_out = f(x, y)
        tangent_out = jnp.cos(x) * x_dot * y + jnp.sin(x) * y_dot
        return primal_out, tangent_out
    """
    self.jvp = jvp
    self.symbolic_zeros = symbolic_zeros
    return jvp

  def defjvps(self, *jvps: Callable[..., ReturnValue] | None):
    """Convenience wrapper for defining JVPs for each argument separately.

    This convenience wrapper cannot be used together with ``nondiff_argnums``.

    Args:
      *jvps: a sequence of functions, one for each positional argument of the
        ``custom_jvp`` function. Each function takes as arguments the tangent
        value for the corresponding primal input, the primal output, and the
        primal inputs. See the example below.

    Returns:
      None.

    Example::

      @jax.custom_jvp
      def f(x, y):
        return jnp.sin(x) * y

      f.defjvps(lambda x_dot, primal_out, x, y: jnp.cos(x) * x_dot * y,
                lambda y_dot, primal_out, x, y: jnp.sin(x) * y_dot)
    """
    if self.nondiff_argnums:
      raise TypeError("Can't use ``defjvps`` with ``nondiff_argnums``.")

    def jvp(primals, tangents):
      primal_out = self(*primals)
      zeros = _zeros_like_pytree(primal_out)
      all_tangents_out = [jvp(t, primal_out, *primals) if jvp else zeros
                          for t, jvp in zip(tangents, jvps)]
      tangent_out = tree_map(_sum_tangents, primal_out, *all_tangents_out)
      return primal_out, tangent_out

    self.defjvp(jvp)

  @traceback_util.api_boundary
  def __call__(self, *args: Any, **kwargs: Any) -> ReturnValue:  # pytype: disable=invalid-annotation
    primal_name = getattr(self.fun, '__name__', str(self.fun))
    if not self.jvp:
      msg = f"No JVP defined for custom_jvp function {primal_name} using defjvp."
      raise AttributeError(msg)
    jvp_name    = getattr(self.jvp, '__name__', str(self.jvp))
    args = _resolve_kwargs(self.fun, args, kwargs)
    if self.nondiff_argnums:
      nondiff_argnums = set(self.nondiff_argnums)
      args = tuple(_stop_gradient(x) if i in nondiff_argnums else x
                   for i, x in enumerate(args))
      diff_argnums = [i for i in range(len(args)) if i not in nondiff_argnums]
      f_, dyn_args = argnums_partial(lu.wrap_init(self.fun), diff_argnums, args,
                                     require_static_args_hashable=False)
      static_args = [args[i] for i in self.nondiff_argnums]
      jvp = _add_args(lu.wrap_init(self.jvp), static_args)
    else:
      f_, dyn_args = lu.wrap_init(self.fun), args  # type: ignore
      jvp = lu.wrap_init(self.jvp)
    args_flat, in_tree = tree_flatten(dyn_args)
    flat_fun, out_type1 = _flatten_fun_nokwargs(f_, in_tree)
    flat_jvp, out_type2 = _flatten_jvp(jvp, primal_name, jvp_name, in_tree,
                                       out_type1)
    out_flat = custom_jvp_call_p.bind(flat_fun, flat_jvp, *args_flat,
                                      symbolic_zeros=self.symbolic_zeros)
    _, (out_tree, _) = lu.merge_linear_aux(out_type1, out_type2)
    return tree_unflatten(out_tree, out_flat)
