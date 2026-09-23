def compress(condition: ArrayLike, a: ArrayLike, axis: int | None = None,
             *, size: int | None = None, fill_value: ArrayLike = 0, out: None = None) -> Array:
  """Compress an array along a given axis using a boolean condition.

  JAX implementation of :func:`numpy.compress`.

  Args:
    condition: 1-dimensional array of conditions. Will be converted to boolean.
    a: N-dimensional array of values.
    axis: axis along which to compress. If None (default) then ``a`` will be
      flattened, and axis will be set to 0.
    size: optional static size for output. Must be specified in order for ``compress``
      to be compatible with JAX transformations like :func:`~jax.jit` or :func:`~jax.vmap`.
    fill_value: if ``size`` is specified, fill padded entries with this value (default: 0).
    out: not implemented by JAX.

  Returns:
    An array of dimension ``a.ndim``, compressed along the specified axis.

  See also:
    - :func:`jax.numpy.extract`: 1D version of ``compress``.
    - :meth:`jax.Array.compress`: equivalent functionality as an array method.

  Notes:
    This function does not require strict shape agreement between ``condition`` and ``a``.
    If ``condition.size > a.shape[axis]``, then ``condition`` will be truncated, and if
    ``a.shape[axis] > condition.size``, then ``a`` will be truncated.

  Examples:
    Compressing along the rows of a 2D array:

    >>> a = jnp.array([[1,  2,  3,  4],
    ...                [5,  6,  7,  8],
    ...                [9,  10, 11, 12]])
    >>> condition = jnp.array([True, False, True])
    >>> jnp.compress(condition, a, axis=0)
    Array([[ 1,  2,  3,  4],
           [ 9, 10, 11, 12]], dtype=int32)

    For convenience, you can equivalently use the :meth:`~jax.Array.compress`
    method of JAX arrays:

    >>> a.compress(condition, axis=0)
    Array([[ 1,  2,  3,  4],
           [ 9, 10, 11, 12]], dtype=int32)

    Note that the condition need not match the shape of the specified axis;
    here we compress the columns with the length-3 condition. Values beyond
    the size of the condition are ignored:

    >>> jnp.compress(condition, a, axis=1)
    Array([[ 1,  3],
           [ 5,  7],
           [ 9, 11]], dtype=int32)

    The optional ``size`` argument lets you specify a static output size so
    that the output is statically-shaped, and so this function can be used
    with transformations like :func:`~jax.jit` and :func:`~jax.vmap`:

    >>> f = lambda c, a: jnp.extract(c, a, size=len(a), fill_value=0)
    >>> mask = (a % 3 == 0)
    >>> jax.vmap(f)(mask, a)
    Array([[ 3,  0,  0,  0],
           [ 6,  0,  0,  0],
           [ 9, 12,  0,  0]], dtype=int32)
  """
  util.check_arraylike("compress", condition, a, fill_value)
  condition_arr = asarray(condition).astype(bool)
  if out is not None:
    raise NotImplementedError("The 'out' argument to jnp.compress is not supported.")
  if condition_arr.ndim != 1:
    raise ValueError("condition must be a 1D array")
  if axis is None:
    axis = 0
    arr = ravel(a)
  else:
    arr = moveaxis(a, axis, 0)
  condition_arr, extra = condition_arr[:arr.shape[0]], condition_arr[arr.shape[0]:]
  arr = arr[:condition_arr.shape[0]]

  if size is None:
    if reductions.any(extra):
      raise ValueError("condition contains entries that are out of bounds")
    result = arr[condition_arr]
  elif not 0 <= size <= arr.shape[0]:
    raise ValueError("size must be positive and not greater than the size of the array axis;"
                     f" got {size=} for a.shape[axis]={arr.shape[0]}")
  else:
    mask = expand_dims(condition_arr, range(1, arr.ndim))
    arr = where(mask, arr, array(fill_value, dtype=arr.dtype))
    result = arr[argsort(condition_arr, stable=True, descending=True)][:size]
  return moveaxis(result, 0, axis)
