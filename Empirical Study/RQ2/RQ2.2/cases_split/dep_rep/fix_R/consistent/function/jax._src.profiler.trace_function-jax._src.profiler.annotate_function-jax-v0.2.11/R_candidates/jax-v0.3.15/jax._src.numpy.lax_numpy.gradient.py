@_wraps(np.gradient, skip_params=['edge_order'])
@partial(jit, static_argnames=('axis', 'edge_order'))
def gradient(f, *varargs, axis: Optional[Union[int, Tuple[int, ...]]] = None,
             edge_order=None):
  if edge_order is not None:
    raise NotImplementedError("The 'edge_order' argument to jnp.gradient is not supported.")

  def gradient_along_axis(a, h, axis):
    sliced = partial(lax.slice_in_dim, a, axis=axis)
    a_grad = concatenate((
      (sliced(1, 2) - sliced(0, 1)),  # upper edge
      (sliced(2, None) - sliced(None, -2)) * 0.5,  # inner
      (sliced(-1, None) - sliced(-2, -1)),  # lower edge
    ), axis)
    return a_grad / h

  a = f
  axis_tuple: Tuple[int, ...]
  if axis is None:
    axis_tuple = tuple(range(a.ndim))
  else:
    if isinstance(axis, int):
      axis = (axis,)
    elif not isinstance(axis, tuple) and not isinstance(axis, list):
      raise ValueError("Give `axis` either as int or iterable")
    elif len(axis) == 0:
      return []
    axis_tuple = tuple(_canonicalize_axis(i, a.ndim) for i in axis)

  if _min([s for i, s in enumerate(a.shape) if i in axis_tuple]) < 2:
    raise ValueError("Shape of array too small to calculate "
                     "a numerical gradient, "
                     "at least 2 elements are required.")
  len_axes = len(axis_tuple)
  n = len(varargs)
  if n == 0 or varargs is None:
    # no spacing
    dx = [1.0] * len_axes
  elif n == 1:
    # single value for all axes
    dx = list(varargs) * len_axes
  elif n == len_axes:
    dx = list(varargs)
  else:
    TypeError("Invalid number of spacing arguments %d" % n)

  if ndim(dx[0]) != 0:
    raise NotImplementedError("Non-constant spacing not implemented")

  # TODO: use jax.lax loop tools if possible
  a_grad = [gradient_along_axis(a, h, ax) for ax, h in zip(axis_tuple, dx)]

  if len(axis_tuple) == 1:
    a_grad = a_grad[0]

  return a_grad
