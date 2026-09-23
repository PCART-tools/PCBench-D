@_wraps(np.linalg.multi_dot)
def multi_dot(arrays, *, precision=None):
  check_arraylike('jnp.linalg.multi_dot', *arrays)
  n = len(arrays)
  # optimization only makes sense for len(arrays) > 2
  if n < 2:
    raise ValueError("Expecting at least two arrays.")
  elif n == 2:
    return jnp.dot(arrays[0], arrays[1], precision=precision)

  arrays = [jnp.asarray(a) for a in arrays]

  # save original ndim to reshape the result array into the proper form later
  ndim_first, ndim_last = arrays[0].ndim, arrays[-1].ndim
  # Explicitly convert vectors to 2D arrays to keep the logic of the internal
  # _multi_dot_* functions as simple as possible.
  if arrays[0].ndim == 1:
    arrays[0] = jnp.atleast_2d(arrays[0])
  if arrays[-1].ndim == 1:
    arrays[-1] = jnp.atleast_2d(arrays[-1]).T
  _assert2d(*arrays)

  # _multi_dot_three is much faster than _multi_dot_matrix_chain_order
  if n == 3:
    result = _multi_dot_three(*arrays, precision)
  else:
    order = _multi_dot_matrix_chain_order(arrays)
    result = _multi_dot(arrays, order, 0, n - 1, precision)

  # return proper shape
  if ndim_first == 1 and ndim_last == 1:
    return result[0, 0]  # scalar
  elif ndim_first == 1 or ndim_last == 1:
    return result.ravel()  # 1-D
  else:
    return result
