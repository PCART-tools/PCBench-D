@_wraps(np.count_nonzero)
@partial(api.jit, static_argnames=('axis', 'keepdims'))
def count_nonzero(a: ArrayLike, axis: Axis = None,
                  keepdims: bool = False) -> Array:
  check_arraylike("count_nonzero", a)
  return sum(lax.ne(a, _lax_const(a, 0)), axis=axis,
             dtype=dtypes.canonicalize_dtype(np.int_), keepdims=keepdims)
