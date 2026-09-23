def _nan_reduction(a: ArrayLike, name: str, jnp_reduction: Callable[..., Array],
                   init_val: ArrayLike, nan_if_all_nan: bool,
                   axis: Axis = None, keepdims: bool = False, **kwargs) -> Array:
  check_arraylike(name, a)
  if not dtypes.issubdtype(dtypes.dtype(a), np.inexact):
    return jnp_reduction(a, axis=axis, keepdims=keepdims, **kwargs)

  out = jnp_reduction(_where(lax_internal._isnan(a), _reduction_init_val(a, init_val), a),
                      axis=axis, keepdims=keepdims, **kwargs)
  if nan_if_all_nan:
    return _where(all(lax_internal._isnan(a), axis=axis, keepdims=keepdims),
                  _lax_const(a, np.nan), out)
  else:
    return out
