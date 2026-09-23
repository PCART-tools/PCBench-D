def _hessenberg_abstract_eval(a):
  if a.dtype not in (jnp.float32, jnp.float64, jnp.complex64, jnp.complex128):
    raise TypeError("hessenberg requires a.dtype to be float32, float64, "
                    f"complex64, or complex128, got {a.dtype}.")
  if a.ndim < 2:
    raise TypeError("hessenberg requires a.ndim to be at least 2, got "
                    f"{a.ndim}.")
  if a.shape[-1] != a.shape[-2]:
    raise TypeError("hessenberg requires the last two dimensions of a to be "
                    f"equal in size, got a.shape of {a.shape}.")
  return [a, ShapedArray(a.shape[:-2] + (a.shape[-1] - 1,), a.dtype)]
