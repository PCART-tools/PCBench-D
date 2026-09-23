def _tridiagonal_abstract_eval(a, *, lower):
  if a.dtype not in (jnp.float32, jnp.float64, jnp.complex64, jnp.complex128):
    raise TypeError("tridiagonal requires a.dtype to be float32, float64, "
                    f"complex64, or complex128, got {a.dtype}.")
  if a.ndim < 2:
    raise TypeError("tridiagonal requires a.ndim to be at least 2, got "
                    f"{a.ndim}.")
  if a.shape[-1] != a.shape[-2]:
    raise TypeError("tridiagonal requires the last two dimensions of a to be "
                    f"equal in size, got a.shape of {a.shape}.")
  if a.shape[-1] == 0:
    raise TypeError("tridiagonal requires the last two dimensions of a to be "
                    f"non-zero, got a.shape of {a.shape}.")
  real_dtype = jnp.finfo(a.dtype).dtype
  return [
      a,
      ShapedArray(a.shape[:-2] + (a.shape[-1],), real_dtype),
      ShapedArray(a.shape[:-2] + (a.shape[-1] - 1,), real_dtype),
      ShapedArray(a.shape[:-2] + (a.shape[-1] - 1,), a.dtype),
      ShapedArray(a.shape[:-2], np.int32)
  ]
