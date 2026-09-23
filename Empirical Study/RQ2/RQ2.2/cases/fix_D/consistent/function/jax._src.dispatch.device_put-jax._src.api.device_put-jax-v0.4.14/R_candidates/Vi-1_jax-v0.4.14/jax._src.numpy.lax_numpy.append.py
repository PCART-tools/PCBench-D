@util._wraps(np.append)
@partial(jit, static_argnames=('axis',))
def append(arr, values, axis: Optional[int] = None):
  if axis is None:
    return concatenate([ravel(arr), ravel(values)], 0)
  else:
    return concatenate([arr, values], axis=axis)
