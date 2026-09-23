@_wraps(np.count_nonzero)
@partial(api.jit, static_argnames=('axis', 'keepdims'))
def count_nonzero(a, axis: Optional[Union[int, Tuple[int, ...]]] = None,
                  keepdims=False):
  _check_arraylike("count_nonzero", a)
  return sum(lax.ne(a, _lax_const(a, 0)), axis=axis,
             dtype=dtypes.canonicalize_dtype(np.int_), keepdims=keepdims)
