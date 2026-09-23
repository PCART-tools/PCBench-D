@_wraps(np.roots, lax_description="""\
Unlike the numpy version of this function, the JAX version returns the roots in
a complex array regardless of the values of the roots. Additionally, the jax
version of this function adds the ``strip_zeros`` function which must be set to
False for the function to be compatible with JIT and other JAX transformations.
With ``strip_zeros=False``, if your coefficients have leading zeros, the
roots will be padded with NaN values:

>>> coeffs = jnp.array([0, 1, 2])

# The default behavior matches numpy and strips leading zeros:
>>> jnp.roots(coeffs)
Array([-2.+0.j], dtype=complex64)

# With strip_zeros=False, extra roots are set to NaN:
>>> jnp.roots(coeffs, strip_zeros=False)
Array([-2. +0.j, nan+nanj], dtype=complex64)
""",
extra_params="""
strip_zeros : bool, default=True
    If set to True, then leading zeros in the coefficients will be stripped, similar
    to :func:`numpy.roots`. If set to False, leading zeros will not be stripped, and
    undefined roots will be represented by NaN values in the function output.
    ``strip_zeros`` must be set to ``False`` for the function to be compatible with
    :func:`jax.jit` and other JAX transformations.
""")
def roots(p: ArrayLike, *, strip_zeros: bool = True) -> Array:
  _check_arraylike("roots", p)
  p_arr = atleast_1d(*_promote_dtypes_inexact(p))
  if p_arr.ndim != 1:
    raise ValueError("Input must be a rank-1 array.")
  if p_arr.size < 2:
    return array([], dtype=dtypes.to_complex_dtype(p_arr.dtype))
  num_leading_zeros = _where(all(p_arr == 0), len(p_arr), argmin(p_arr == 0))

  if strip_zeros:
    num_leading_zeros = core.concrete_or_error(int, num_leading_zeros,
      "The error occurred in the jnp.roots() function. To use this within a "
      "JIT-compiled context, pass strip_zeros=False, but be aware that leading zeros "
      "will be result in some returned roots being set to NaN.")
    return _roots_no_zeros(p_arr[num_leading_zeros:])
  else:
    return _roots_with_zeros(p_arr, num_leading_zeros)
