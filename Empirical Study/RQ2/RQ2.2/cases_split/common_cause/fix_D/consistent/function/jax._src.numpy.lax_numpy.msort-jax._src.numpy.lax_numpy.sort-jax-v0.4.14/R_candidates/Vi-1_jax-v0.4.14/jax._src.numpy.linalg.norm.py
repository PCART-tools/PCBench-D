@_wraps(np.linalg.norm)
@partial(jit, static_argnames=('ord', 'axis', 'keepdims'))
def norm(x: ArrayLike, ord: Union[int, str, None] = None,
         axis: Union[None, tuple[int, ...], int] = None,
         keepdims: bool = False) -> Array:
  check_arraylike("jnp.linalg.norm", x)
  x, = promote_dtypes_inexact(jnp.asarray(x))
  x_shape = jnp.shape(x)
  ndim = len(x_shape)

  if axis is None:
    # NumPy has an undocumented behavior that admits arbitrary rank inputs if
    # `ord` is None: https://github.com/numpy/numpy/issues/14215
    if ord is None:
      return ufuncs.sqrt(reductions.sum(ufuncs.real(x * ufuncs.conj(x)), keepdims=keepdims))
    axis = tuple(range(ndim))
  elif isinstance(axis, tuple):
    axis = tuple(canonicalize_axis(x, ndim) for x in axis)
  else:
    axis = (canonicalize_axis(axis, ndim),)

  num_axes = len(axis)
  if num_axes == 1:
    if ord is None or ord == 2:
      return ufuncs.sqrt(reductions.sum(ufuncs.real(x * ufuncs.conj(x)), axis=axis,
                                        keepdims=keepdims))
    elif ord == jnp.inf:
      return reductions.amax(ufuncs.abs(x), axis=axis, keepdims=keepdims)
    elif ord == -jnp.inf:
      return reductions.amin(ufuncs.abs(x), axis=axis, keepdims=keepdims)
    elif ord == 0:
      return reductions.sum(x != 0, dtype=jnp.finfo(lax.dtype(x)).dtype,
                            axis=axis, keepdims=keepdims)
    elif ord == 1:
      # Numpy has a special case for ord == 1 as an optimization. We don't
      # really need the optimization (XLA could do it for us), but the Numpy
      # code has slightly different type promotion semantics, so we need a
      # special case too.
      return reductions.sum(ufuncs.abs(x), axis=axis, keepdims=keepdims)
    elif isinstance(ord, str):
      msg = f"Invalid order '{ord}' for vector norm."
      if ord == "inf":
        msg += "Use 'jax.numpy.inf' instead."
      if ord == "-inf":
        msg += "Use '-jax.numpy.inf' instead."
      raise ValueError(msg)
    else:
      abs_x = ufuncs.abs(x)
      ord_arr = lax_internal._const(abs_x, ord)
      ord_inv = lax_internal._const(abs_x, 1. / ord_arr)
      out = reductions.sum(abs_x ** ord_arr, axis=axis, keepdims=keepdims)
      return ufuncs.power(out, ord_inv)

  elif num_axes == 2:
    row_axis, col_axis = cast(tuple[int, ...], axis)
    if ord is None or ord in ('f', 'fro'):
      return ufuncs.sqrt(reductions.sum(ufuncs.real(x * ufuncs.conj(x)), axis=axis,
                                        keepdims=keepdims))
    elif ord == 1:
      if not keepdims and col_axis > row_axis:
        col_axis -= 1
      return reductions.amax(reductions.sum(ufuncs.abs(x), axis=row_axis, keepdims=keepdims),
                             axis=col_axis, keepdims=keepdims)
    elif ord == -1:
      if not keepdims and col_axis > row_axis:
        col_axis -= 1
      return reductions.amin(reductions.sum(ufuncs.abs(x), axis=row_axis, keepdims=keepdims),
                             axis=col_axis, keepdims=keepdims)
    elif ord == jnp.inf:
      if not keepdims and row_axis > col_axis:
        row_axis -= 1
      return reductions.amax(reductions.sum(ufuncs.abs(x), axis=col_axis, keepdims=keepdims),
                     axis=row_axis, keepdims=keepdims)
    elif ord == -jnp.inf:
      if not keepdims and row_axis > col_axis:
        row_axis -= 1
      return reductions.amin(reductions.sum(ufuncs.abs(x), axis=col_axis, keepdims=keepdims),
                     axis=row_axis, keepdims=keepdims)
    elif ord in ('nuc', 2, -2):
      x = jnp.moveaxis(x, axis, (-2, -1))
      if ord == 2:
        reducer = reductions.amax
      elif ord == -2:
        reducer = reductions.amin
      else:
        # `sum` takes an extra dtype= argument, unlike `amax` and `amin`.
        reducer = reductions.sum  # type: ignore[assignment]
      y = reducer(svd(x, compute_uv=False), axis=-1)
      if keepdims:
        y = jnp.expand_dims(y, axis)
      return y
    else:
      raise ValueError(f"Invalid order '{ord}' for matrix norm.")
  else:
    raise ValueError(
        f"Invalid axis values ({axis}) for jnp.linalg.norm.")
