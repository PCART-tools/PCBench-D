@jit
def poly(seq_of_zeros: ArrayLike) -> Array:
  r"""Returns the coefficients of a polynomial for the given sequence of roots.

  JAX implementation of :func:`numpy.poly`.

  Args:
    seq_of_zeros: A scalar or an array of roots of the polynomial of shape ``(M,)``
      or ``(M, M)``.

  Returns:
    An array containing the coefficients of the polynomial. The dtype of the
    output is always promoted to inexact.

  Note:

    :func:`jax.numpy.poly` differs from :func:`numpy.poly`:

    - When the input is a scalar, ``np.poly`` raises a ``TypeError``, whereas
      ``jnp.poly`` treats scalars the same as length-1 arrays.
    - For complex-valued or square-shaped inputs, ``jnp.poly`` always returns
      complex coefficients, whereas ``np.poly`` may return real or complex
      depending on their values.

  See also:
    - :func:`jax.numpy.polyfit`: Least squares polynomial fit.
    - :func:`jax.numpy.polyval`: Evaluate a polynomial at specific values.
    - :func:`jax.numpy.roots`: Computes the roots of a polynomial for given
      coefficients.

  Example:

    Scalar inputs:

    >>> jnp.poly(1)
    Array([ 1., -1.], dtype=float32)

    Input array with integer values:

    >>> x = jnp.array([1, 2, 3])
    >>> jnp.poly(x)
    Array([ 1., -6., 11., -6.], dtype=float32)

    Input array with complex conjugates:

    >>> x = jnp.array([2, 1+2j, 1-2j])
    >>> jnp.poly(x)
    Array([  1.+0.j,  -4.+0.j,   9.+0.j, -10.+0.j], dtype=complex64)

    Input array as square matrix with real valued inputs:

    >>> x = jnp.array([[2, 1, 5],
    ...                [3, 4, 7],
    ...                [1, 3, 5]])
    >>> jnp.round(jnp.poly(x))
    Array([  1.+0.j, -11.-0.j,   9.+0.j, -15.+0.j], dtype=complex64)
  """
  check_arraylike('poly', seq_of_zeros)
  seq_of_zeros, = promote_dtypes_inexact(seq_of_zeros)
  seq_of_zeros_arr = atleast_1d(seq_of_zeros)
  del seq_of_zeros

  sh = seq_of_zeros_arr.shape
  if len(sh) == 2 and sh[0] == sh[1] and sh[0] != 0:
    # import at runtime to avoid circular import
    from jax._src.numpy import linalg
    seq_of_zeros_arr = linalg.eigvals(seq_of_zeros_arr)

  if seq_of_zeros_arr.ndim != 1:
    raise ValueError("input must be 1d or non-empty square 2d array.")

  dt = seq_of_zeros_arr.dtype
  if len(seq_of_zeros_arr) == 0:
    return ones((), dtype=dt)

  a = ones((1,), dtype=dt)
  for k in range(len(seq_of_zeros_arr)):
    a = convolve(a, array([1, -seq_of_zeros_arr[k]], dtype=dt), mode='full')

  return a
