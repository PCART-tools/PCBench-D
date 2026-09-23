@implements(np.nanmin, skip_params=['out'])
@partial(api.jit, static_argnames=('axis', 'keepdims'))
def nanmin(a: ArrayLike, axis: Axis = None, out: None = None,
           keepdims: bool = False, initial: ArrayLike | None = None,
           where: ArrayLike | None = None) -> Array:
  return _nan_reduction(a, 'nanmin', min, np.inf, nan_if_all_nan=initial is None,
                        axis=axis, out=out, keepdims=keepdims,
                        initial=initial, where=where)
