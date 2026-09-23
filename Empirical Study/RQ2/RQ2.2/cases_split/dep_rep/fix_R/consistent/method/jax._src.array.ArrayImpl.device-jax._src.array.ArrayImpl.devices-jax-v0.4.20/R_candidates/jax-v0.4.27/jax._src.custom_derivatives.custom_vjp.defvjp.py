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
