def dynamic_update_slice(operand: Array | np.ndarray, update: ArrayLike,
                         start_indices: Array | Sequence[ArrayLike]) -> Array:
  """Wraps XLA's `DynamicUpdateSlice
  <https://www.tensorflow.org/xla/operation_semantics#dynamicupdateslice>`_
  operator.

  Args:
    operand: an array to slice.
    update: an array containing the new values to write onto `operand`.
    start_indices: a list of scalar indices, one per dimension.

  Returns:
    An array containing the slice.

  Examples:
    Here is an example of updating a one-dimensional slice update:

    >>> x = jnp.zeros(6)
    >>> y = jnp.ones(3)
    >>> dynamic_update_slice(x, y, (2,))
    Array([0., 0., 1., 1., 1., 0.], dtype=float32)

    If the update slice is too large to fit in the array, the start
    index will be adjusted to make it fit

    >>> dynamic_update_slice(x, y, (3,))
    Array([0., 0., 0., 1., 1., 1.], dtype=float32)
    >>> dynamic_update_slice(x, y, (5,))
    Array([0., 0., 0., 1., 1., 1.], dtype=float32)

    Here is an example of a two-dimensional slice update:

    >>> x = jnp.zeros((4, 4))
    >>> y = jnp.ones((2, 2))
    >>> dynamic_update_slice(x, y, (1, 2))
    Array([[0., 0., 0., 0.],
           [0., 0., 1., 1.],
           [0., 0., 1., 1.],
           [0., 0., 0., 0.]], dtype=float32)

  See Also:
    - :attr:`jax.numpy.ndarray.at`
    - :attr:`lax.dynamic_update_index_in_dim`
    - :attr:`lax.dynamic_update_slice_in_dim`
  """
  start_indices = _dynamic_slice_indices(operand, start_indices)
  return dynamic_update_slice_p.bind(operand, update, *start_indices)
