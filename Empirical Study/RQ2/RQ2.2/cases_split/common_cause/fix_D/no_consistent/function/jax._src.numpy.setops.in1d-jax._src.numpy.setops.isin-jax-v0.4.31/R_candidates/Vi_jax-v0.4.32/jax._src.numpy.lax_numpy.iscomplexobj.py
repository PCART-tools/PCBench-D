def iscomplexobj(x: Any) -> bool:
  """Check if the input is a complex number or an array containing complex elements.

  JAX implementation of :func:`numpy.iscomplexobj`.

  The function evaluates based on input type rather than value.
  Inputs with zero imaginary parts are still considered complex.

  Args:
    x: input object to check.

  Returns:
    True if ``x`` is a complex number or an array containing at least one complex element,
    False otherwise.

  See Also:
    - :func:`jax.numpy.isrealobj`
    - :func:`jax.numpy.iscomplex`

  Examples:
    >>> jnp.iscomplexobj(True)
    False
    >>> jnp.iscomplexobj(0)
    False
    >>> jnp.iscomplexobj(jnp.array([1, 2]))
    False
    >>> jnp.iscomplexobj(1+2j)
    True
    >>> jnp.iscomplexobj(jnp.array([0, 1+2j]))
    True
  """
  if x is None:
    return False
  try:
    typ = x.dtype.type
  except AttributeError:
    typ = asarray(x).dtype.type
  return issubdtype(typ, complexfloating)
