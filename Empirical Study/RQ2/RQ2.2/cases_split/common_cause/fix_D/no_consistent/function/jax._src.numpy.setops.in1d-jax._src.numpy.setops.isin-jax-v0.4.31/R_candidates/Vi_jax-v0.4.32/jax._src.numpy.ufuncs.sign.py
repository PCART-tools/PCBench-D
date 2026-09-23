@partial(jit, inline=True)
def sign(x: ArrayLike, /) -> Array:
  r"""Return an element-wise indication of sign of the input.

  JAX implementation of :obj:`numpy.sign`.

  The sign of ``x`` for real-valued input is:

  .. math::
    \mathrm{sign}(x) = \begin{cases}
      1, & x > 0\\
      0, & x = 0\\
      -1, & x < 0
    \end{cases}

  For complex valued input, ``jnp.sign`` returns a unit vector repesenting the
  phase. For generalized case, the sign of ``x`` is given by:

  .. math::
    \mathrm{sign}(x) = \begin{cases}
      \frac{x}{abs(x)}, & x \ne 0\\
      0, & x = 0
    \end{cases}

  Args:
    x: input array or scalar.

  Returns:
    An array with same shape and dtype as ``x`` containing the sign indication.

  See also:
    - :func:`jax.numpy.positive`: Returns element-wise positive values of the input.
    - :func:`jax.numpy.negative`: Returns element-wise negative values of the input.

  Examples:
    For Real-valued inputs:

    >>> x = jnp.array([0., -3., 7.])
    >>> jnp.sign(x)
    Array([ 0., -1.,  1.], dtype=float32)

    For complex-inputs:

    >>> x1 = jnp.array([1, 3+4j, 5j])
    >>> jnp.sign(x1)
    Array([1. +0.j , 0.6+0.8j, 0. +1.j ], dtype=complex64)
  """
  return lax.sign(*promote_args('sign', x))
