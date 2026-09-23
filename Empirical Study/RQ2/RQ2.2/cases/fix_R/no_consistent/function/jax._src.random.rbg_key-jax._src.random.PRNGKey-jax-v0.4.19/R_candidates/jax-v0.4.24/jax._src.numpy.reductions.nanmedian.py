@implements(np.nanmedian, skip_params=['out', 'overwrite_input'])
@partial(api.jit, static_argnames=('axis', 'overwrite_input', 'keepdims'))
def nanmedian(a: ArrayLike, axis: int | tuple[int, ...] | None = None,
              out: None = None, overwrite_input: bool = False,
              keepdims: bool = False) -> Array:
  check_arraylike("nanmedian", a)
  return nanquantile(a, 0.5, axis=axis, out=out,
                     overwrite_input=overwrite_input, keepdims=keepdims,
                     method='midpoint')
