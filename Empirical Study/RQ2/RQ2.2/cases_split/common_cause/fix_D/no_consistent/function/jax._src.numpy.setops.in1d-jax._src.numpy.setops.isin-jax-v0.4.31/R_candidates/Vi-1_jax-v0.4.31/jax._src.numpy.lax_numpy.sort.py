@partial(jit, static_argnames=('axis', 'kind', 'order', 'stable', 'descending'))
def sort(
    a: ArrayLike,
    axis: int | None = -1,
    *,
    kind: None = None,
    order: None = None,
    stable: bool = True,
    descending: bool = False,
) -> Array:
  """Return a sorted copy of an array.

  JAX implementation of :func:`numpy.sort`.

  Args:
    a: array to sort
    axis: integer axis along which to sort. Defaults to ``-1``, i.e. the last
      axis. If ``None``, then ``a`` is flattened before being sorted.
    stable: boolean specifying whether a stable sort should be used. Default=True.
    descending: boolean specifying whether to sort in descending order. Default=False.
    kind: deprecated; instead specify sort algorithm using stable=True or stable=False.
    order: not supported by JAX

  Returns:
    Sorted array of shape ``a.shape`` (if ``axis`` is an integer) or of shape
    ``(a.size,)`` (if ``axis`` is None).

  Examples:
    Simple 1-dimensional sort

    >>> x = jnp.array([1, 3, 5, 4, 2, 1])
    >>> jnp.sort(x)
    Array([1, 1, 2, 3, 4, 5], dtype=int32)

    Sort along the last axis of an array:

    >>> x = jnp.array([[2, 1, 3],
    ...                [4, 3, 6]])
    >>> jnp.sort(x, axis=1)
    Array([[1, 2, 3],
           [3, 4, 6]], dtype=int32)

  See also:
    - :func:`jax.numpy.argsort`: return indices of sorted values.
    - :func:`jax.numpy.lexsort`: lexicographical sort of multiple arrays.
    - :func:`jax.lax.sort`: lower-level function wrapping XLA's Sort operator.
  """
  util.check_arraylike("sort", a)
  if kind is not None:
    raise TypeError("'kind' argument to sort is not supported. Use"
                    " stable=True or stable=False to specify sort stability.")
  if order is not None:
    raise TypeError("'order' argument to sort is not supported.")
  if axis is None:
    arr = ravel(a)
    axis = 0
  else:
    arr = asarray(a)
  dimension = _canonicalize_axis(axis, arr.ndim)
  result = lax.sort(arr, dimension=dimension, is_stable=stable)
  return lax.rev(result, dimensions=[dimension]) if descending else result
