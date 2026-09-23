@partial(jit, static_argnames=['deg'])
def angle(z: ArrayLike, deg: bool = False) -> Array:
  """Return the angle of a complex valued number or array.

  JAX implementation of :func:`numpy.angle`.

  Args:
    z: A complex number or an array of complex numbers.
    deg: Boolean. If ``True``, returns the result in degrees else returns
      in radians. Default is ``False``.

  Returns:
    An array of counterclockwise angle of each element of ``z``, with the same
    shape as ``z`` of dtype float.

  Examples:

    If ``z`` is a number

    >>> z1 = 2+3j
    >>> jnp.angle(z1)
    Array(0.98279375, dtype=float32, weak_type=True)

    If ``z`` is an array

    >>> z2 = jnp.array([[1+3j, 2-5j],
    ...                 [4-3j, 3+2j]])
    >>> with jnp.printoptions(precision=2, suppress=True):
    ...     print(jnp.angle(z2))
    [[ 1.25 -1.19]
     [-0.64  0.59]]

    If ``deg=True``.

    >>> with jnp.printoptions(precision=2, suppress=True):
    ...     print(jnp.angle(z2, deg=True))
    [[ 71.57 -68.2 ]
     [-36.87  33.69]]
  """
  re = ufuncs.real(z)
  im = ufuncs.imag(z)
  dtype = _dtype(re)
  if not issubdtype(dtype, inexact) or (
      issubdtype(_dtype(z), floating) and ndim(z) == 0):
    dtype = dtypes.canonicalize_dtype(float_)
    re = lax.convert_element_type(re, dtype)
    im = lax.convert_element_type(im, dtype)
  result = lax.atan2(im, re)
  return ufuncs.degrees(result) if deg else result
