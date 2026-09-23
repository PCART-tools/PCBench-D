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
