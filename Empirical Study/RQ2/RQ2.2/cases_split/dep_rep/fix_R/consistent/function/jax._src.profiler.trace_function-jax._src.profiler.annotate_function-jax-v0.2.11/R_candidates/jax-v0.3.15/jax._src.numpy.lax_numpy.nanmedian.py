@_wraps(np.nanmedian, skip_params=['out', 'overwrite_input'])
@partial(jit, static_argnames=('axis', 'overwrite_input', 'keepdims'))
def nanmedian(a, axis: Optional[Union[int, Tuple[int, ...]]] = None, out=None,
              overwrite_input=False, keepdims=False):
  _check_arraylike("nanmedian", a)
  return nanquantile(a, 0.5, axis=axis, out=out,
                     overwrite_input=overwrite_input, keepdims=keepdims,
                     method='midpoint')
