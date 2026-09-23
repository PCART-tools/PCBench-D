def _nan_like_mhlo(aval):
  if jnp.issubdtype(aval.dtype, np.complexfloating):
    return mlir.full_like_aval(np.nan + np.nan * 1j, aval)
  else:
    return mlir.full_like_aval(np.nan, aval)
