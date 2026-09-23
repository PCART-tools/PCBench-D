def isrealobj(x: Any) -> bool:
  """Check if the input is not a complex number or an array containing complex elements.

  JAX implementation of :func:`numpy.isrealobj`.

  The function evaluates based on input type rather than value.
  Inputs with zero imaginary parts are still considered complex.

  Args:
    x: input object to check.

  Returns:
    False if ``x`` is a complex number or an array containing at least one complex element,
    True otherwise.

  See Also:
    - :func:`jax.numpy.iscomplexobj`
    - :func:`jax.numpy.isreal`

  Examples:
    >>> jnp.isrealobj(0)
    True
    >>> jnp.isrealobj(1.2)
    True
    >>> jnp.isrealobj(jnp.array([1, 2]))
    True
    >>> jnp.isrealobj(1+2j)
    False
    >>> jnp.isrealobj(jnp.array([0, 1+2j]))
    False
  """
  return not iscomplexobj(x)
