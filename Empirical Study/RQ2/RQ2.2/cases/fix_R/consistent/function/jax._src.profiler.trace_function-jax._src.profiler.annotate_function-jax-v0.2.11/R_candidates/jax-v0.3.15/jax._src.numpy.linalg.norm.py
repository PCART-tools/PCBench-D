@_wraps(np.linalg.norm)
@partial(jit, static_argnames=('ord', 'axis', 'keepdims'))
def norm(x, ord=None, axis : Union[None, Tuple[int, ...], int] = None,
         keepdims=False):
  x, = _promote_dtypes_inexact(jnp.asarray(x))
  x_shape = jnp.shape(x)
  ndim = len(x_shape)

  if axis is None:
    # NumPy has an undocumented behavior that admits arbitrary rank inputs if
    # `ord` is None: https://github.com/numpy/numpy/issues/14215
    if ord is None:
      return jnp.sqrt(jnp.sum(jnp.real(x * jnp.conj(x)), keepdims=keepdims))
    axis = tuple(range(ndim))
  elif isinstance(axis, tuple):
    axis = tuple(canonicalize_axis(x, ndim) for x in axis)
  else:
    axis = (canonicalize_axis(axis, ndim),)

  num_axes = len(axis)
  if num_axes == 1:
    if ord is None or ord == 2:
      return jnp.sqrt(jnp.sum(jnp.real(x * jnp.conj(x)), axis=axis,
                            keepdims=keepdims))
    elif ord == jnp.inf:
      return jnp.amax(jnp.abs(x), axis=axis, keepdims=keepdims)
    elif ord == -jnp.inf:
      return jnp.amin(jnp.abs(x), axis=axis, keepdims=keepdims)
    elif ord == 0:
      return jnp.sum(x != 0, dtype=jnp.finfo(lax.dtype(x)).dtype,
                    axis=axis, keepdims=keepdims)
    elif ord == 1:
      # Numpy has a special case for ord == 1 as an optimization. We don't
      # really need the optimization (XLA could do it for us), but the Numpy
      # code has slightly different type promotion semantics, so we need a
      # special case too.
      return jnp.sum(jnp.abs(x), axis=axis, keepdims=keepdims)
    else:
      abs_x = jnp.abs(x)
      ord = lax_internal._const(abs_x, ord)
      ord_inv = lax_internal._const(abs_x, 1. / ord)
      out = jnp.sum(abs_x ** ord, axis=axis, keepdims=keepdims)
      return jnp.power(out, ord_inv)

  elif num_axes == 2:
    row_axis, col_axis = cast(Tuple[int, ...], axis)
    if ord is None or ord in ('f', 'fro'):
      return jnp.sqrt(jnp.sum(jnp.real(x * jnp.conj(x)), axis=axis,
                            keepdims=keepdims))
    elif ord == 1:
      if not keepdims and col_axis > row_axis:
        col_axis -= 1
      return jnp.amax(jnp.sum(jnp.abs(x), axis=row_axis, keepdims=keepdims),
                     axis=col_axis, keepdims=keepdims)
    elif ord == -1:
      if not keepdims and col_axis > row_axis:
        col_axis -= 1
      return jnp.amin(jnp.sum(jnp.abs(x), axis=row_axis, keepdims=keepdims),
                     axis=col_axis, keepdims=keepdims)
    elif ord == jnp.inf:
      if not keepdims and row_axis > col_axis:
        row_axis -= 1
      return jnp.amax(jnp.sum(jnp.abs(x), axis=col_axis, keepdims=keepdims),
                     axis=row_axis, keepdims=keepdims)
    elif ord == -jnp.inf:
      if not keepdims and row_axis > col_axis:
        row_axis -= 1
      return jnp.amin(jnp.sum(jnp.abs(x), axis=col_axis, keepdims=keepdims),
                     axis=row_axis, keepdims=keepdims)
    elif ord in ('nuc', 2, -2):
      x = jnp.moveaxis(x, axis, (-2, -1))
      if ord == 2:
        reducer = jnp.amax
      elif ord == -2:
        reducer = jnp.amin
      else:
        # `sum` takes an extra dtype= argument, unlike `amax` and `amin`.
        reducer = jnp.sum  # type: ignore[assignment]
      y = reducer(svd(x, compute_uv=False), axis=-1)
      if keepdims:
        y = jnp.expand_dims(y, axis)
      return y
    else:
      raise ValueError(f"Invalid order '{ord}' for matrix norm.")
  else:
    raise ValueError(
        f"Invalid axis values ({axis}) for jnp.linalg.norm.")
