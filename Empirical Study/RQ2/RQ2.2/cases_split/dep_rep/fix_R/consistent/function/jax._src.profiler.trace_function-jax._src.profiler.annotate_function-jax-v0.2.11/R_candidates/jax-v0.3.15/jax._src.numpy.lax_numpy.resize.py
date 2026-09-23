@_wraps(np.resize)
@partial(jit, static_argnames=('new_shape',))
def resize(a, new_shape):
  _check_arraylike("resize", a)
  new_shape = _ensure_index_tuple(new_shape)

  if _any(dim_length < 0 for dim_length in new_shape):
    raise ValueError("all elements of `new_shape` must be non-negative")

  a = ravel(a)

  new_size = _prod(new_shape)
  if a.size == 0 or new_size == 0:
    return zeros_like(a, shape=new_shape)

  repeats = ceil_of_ratio(new_size, a.size)
  a = tile(a, repeats)[:new_size]

  return reshape(a, new_shape)
