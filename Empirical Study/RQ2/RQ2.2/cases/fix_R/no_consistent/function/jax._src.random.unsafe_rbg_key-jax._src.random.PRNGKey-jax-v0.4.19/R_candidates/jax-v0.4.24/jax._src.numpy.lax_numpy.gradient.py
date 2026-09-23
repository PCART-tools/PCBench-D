@util.implements(np.gradient, skip_params=['edge_order'])
@partial(jit, static_argnames=('axis', 'edge_order'))
def gradient(f: ArrayLike, *varargs: ArrayLike,
             axis: int | Sequence[int] | None = None,
             edge_order: int | None = None) -> Array | list[Array]:
  if edge_order is not None:
    raise NotImplementedError("The 'edge_order' argument to jnp.gradient is not supported.")
  a, *spacing = util.promote_args_inexact("gradient", f, *varargs)

  def gradient_along_axis(a, h, axis):
    sliced = partial(lax.slice_in_dim, a, axis=axis)
    a_grad = concatenate((
      (sliced(1, 2) - sliced(0, 1)),  # upper edge
      (sliced(2, None) - sliced(None, -2)) * 0.5,  # inner
      (sliced(-1, None) - sliced(-2, -1)),  # lower edge
    ), axis)
    return a_grad / h

  if axis is None:
    axis_tuple = tuple(range(a.ndim))
  else:
    axis_tuple = tuple(_canonicalize_axis(i, a.ndim) for i in _ensure_index_tuple(axis))
  if len(axis_tuple) == 0:
    return []

  if min([s for i, s in enumerate(a.shape) if i in axis_tuple]) < 2:
    raise ValueError("Shape of array too small to calculate "
                     "a numerical gradient, "
                     "at least 2 elements are required.")
  if len(spacing) == 0:
    dx: Sequence[ArrayLike] = [1.0] * len(axis_tuple)
  elif len(spacing) == 1:
    dx = list(spacing) * len(axis_tuple)
  elif len(spacing) == len(axis_tuple):
    dx = list(spacing)
  else:
    TypeError(f"Invalid number of spacing arguments {len(spacing)} for {axis=}")

  if ndim(dx[0]) != 0:
    raise NotImplementedError("Non-constant spacing not implemented")

  a_grad = [gradient_along_axis(a, h, ax) for ax, h in zip(axis_tuple, dx)]
  return a_grad[0] if len(axis_tuple) == 1 else a_grad
