@util.implements(np.gradient, skip_params=['edge_order'])
@partial(jit, static_argnames=("axis", "edge_order"))
def gradient(
    f: ArrayLike,
    *varargs: ArrayLike,
    axis: int | Sequence[int] | None = None,
    edge_order: int | None = None,
) -> Array | list[Array]:

  if edge_order is not None:
    raise NotImplementedError(
        "The 'edge_order' argument to jnp.gradient is not supported."
    )
  a, *spacing = util.promote_dtypes_inexact(f, *varargs)

  def gradient_along_axis(a, h, axis):
    sliced = partial(lax.slice_in_dim, a, axis=axis)
    upper_edge = sliced(1, 2) - sliced(0, 1)
    lower_edge = sliced(-1, None) - sliced(-2, -1)

    if ndim(h) == 0:
      inner = (sliced(2, None) - sliced(None, -2)) * 0.5 / h
      lower_edge /= h
      upper_edge /= h

    elif ndim(h) == 1:
      if len(h) != a.shape[axis]:
        raise ValueError(
            "Spacing arrays must have the same length as the "
            "dimension along which the gradient is calculated."
        )
      h_shape = [1] * a.ndim
      h_shape[axis] = len(h)
      h = h.reshape(h_shape)
      sliced_x = partial(lax.slice_in_dim, h, axis=axis)

      upper_edge /= sliced_x(1, 2) - sliced_x(0, 1)
      lower_edge /= sliced_x(-1, None) - sliced_x(-2, -1)
      dx1 = sliced_x(1, -1) - sliced_x(0, -2)
      dx2 = sliced_x(2, None) - sliced_x(1, -1)
      a = -(dx2) / (dx1 * (dx1 + dx2))
      b = (dx2 - dx1) / (dx1 * dx2)
      c = dx1 / (dx2 * (dx1 + dx2))
      inner = a * sliced(0, -2) + b * sliced(1, -1) + c * sliced(2, None)
    else:
      raise ValueError("Spacing arrays must be 1D arrays or scalars.")

    return concatenate((upper_edge, inner, lower_edge), axis=axis)

  if axis is None:
    axis_tuple = tuple(range(a.ndim))
  else:
    axis_tuple = tuple(_canonicalize_axis(i, a.ndim) for i in _ensure_index_tuple(axis))
  if len(axis_tuple) == 0:
    return []

  if min(s for i, s in enumerate(a.shape) if i in axis_tuple) < 2:
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

  a_grad = [gradient_along_axis(a, h, ax) for ax, h in zip(axis_tuple, dx)]
  return a_grad[0] if len(axis_tuple) == 1 else a_grad
