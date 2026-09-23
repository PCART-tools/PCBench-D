def tensordot(a: ArrayLike, b: ArrayLike,
              axes: int | Sequence[int] | Sequence[Sequence[int]] = 2,
              *, precision: PrecisionLike = None,
              preferred_element_type: DTypeLike | None = None) -> Array:
  """Compute the tensor dot product of two N-dimensional arrays.

  JAX implementation of :func:`numpy.linalg.tensordot`.

  Args:
    a: N-dimensional array
    b: M-dimensional array
    axes: integer or tuple of sequences of integers. If an integer `k`, then
      sum over the last `k` axes of ``a`` and the first `k` axes of ``b``,
      in order. If a tuple, then ``axes[0]`` specifies the axes of ``a`` and
      ``axes[1]`` specifies the axes of ``b``.
    precision: either ``None`` (default), which means the default precision for
      the backend, a :class:`~jax.lax.Precision` enum value (``Precision.DEFAULT``,
      ``Precision.HIGH`` or ``Precision.HIGHEST``) or a tuple of two
      such values indicating precision of ``a`` and ``b``.
    preferred_element_type: either ``None`` (default), which means the default
      accumulation type for the input types, or a datatype, indicating to
      accumulate results to and return a result with that datatype.

  Returns:
    array containing the tensor dot product of the inputs

  See also:
    - :func:`jax.numpy.einsum`: NumPy API for more general tensor contractions.
    - :func:`jax.lax.dot_general`: XLA API for more general tensor contractions.

  Examples:
    >>> x1 = jnp.arange(24.).reshape(2, 3, 4)
    >>> x2 = jnp.ones((3, 4, 5))
    >>> jnp.tensordot(x1, x2)
    Array([[ 66.,  66.,  66.,  66.,  66.],
           [210., 210., 210., 210., 210.]], dtype=float32)

    Equivalent result when specifying the axes as explicit sequences:

    >>> jnp.tensordot(x1, x2, axes=([1, 2], [0, 1]))
    Array([[ 66.,  66.,  66.,  66.,  66.],
           [210., 210., 210., 210., 210.]], dtype=float32)

    Equivalent result via :func:`~jax.numpy.einsum`:

    >>> jnp.einsum('ijk,jkm->im', x1, x2)
    Array([[ 66.,  66.,  66.,  66.,  66.],
           [210., 210., 210., 210., 210.]], dtype=float32)

    Setting ``axes=1`` for two-dimensional inputs is equivalent to a matrix
    multiplication:

    >>> x1 = jnp.array([[1, 2],
    ...                 [3, 4]])
    >>> x2 = jnp.array([[1, 2, 3],
    ...                 [4, 5, 6]])
    >>> jnp.linalg.tensordot(x1, x2, axes=1)
    Array([[ 9, 12, 15],
           [19, 26, 33]], dtype=int32)
    >>> x1 @ x2
    Array([[ 9, 12, 15],
           [19, 26, 33]], dtype=int32)

    Setting ``axes=0`` for one-dimensional inputs is equivalent to
    :func:`~jax.numpy.outer`:

    >>> x1 = jnp.array([1, 2])
    >>> x2 = jnp.array([1, 2, 3])
    >>> jnp.linalg.tensordot(x1, x2, axes=0)
    Array([[1, 2, 3],
           [2, 4, 6]], dtype=int32)
    >>> jnp.outer(x1, x2)
    Array([[1, 2, 3],
           [2, 4, 6]], dtype=int32)
  """
  util.check_arraylike("tensordot", a, b)
  dtypes.check_user_dtype_supported(preferred_element_type, "tensordot")
  a, b = asarray(a), asarray(b)
  a_ndim = ndim(a)
  b_ndim = ndim(b)

  if preferred_element_type is None:
    preferred_element_type, output_weak_type = dtypes.result_type(a, b, return_weak_type_flag=True)
  else:
    output_weak_type = False

  if type(axes) is int:
    if axes > min(a_ndim, b_ndim):
      msg = "Number of tensordot axes (axes {}) exceeds input ranks ({} and {})"
      raise TypeError(msg.format(axes, a.shape, b.shape))
    contracting_dims = tuple(range(a_ndim - axes, a_ndim)), tuple(range(axes))
  elif isinstance(axes, (tuple, list)) and len(axes) == 2:
    ax1, ax2 = axes
    if type(ax1) == type(ax2) == int:
      contracting_dims = ((_canonicalize_axis(ax1, a_ndim),),
                          (_canonicalize_axis(ax2, b_ndim),))
    elif isinstance(ax1, (tuple, list)) and isinstance(ax2, (tuple, list)):
      if len(ax1) != len(ax2):
        msg = "tensordot requires axes lists to have equal length, got {} and {}."
        raise TypeError(msg.format(ax1, ax2))
      contracting_dims = (tuple(_canonicalize_axis(i, a_ndim) for i in ax1),
                          tuple(_canonicalize_axis(i, b_ndim) for i in ax2))
    else:
      msg = ("tensordot requires both axes lists to be either ints, tuples or "
             "lists, got {} and {}")
      raise TypeError(msg.format(ax1, ax2))
  else:
    msg = ("tensordot axes argument must be an int, a pair of ints, or a pair "
           "of lists/tuples of ints.")
    raise TypeError(msg)
  result = lax.dot_general(a, b, (contracting_dims, ((), ())),
                           precision=precision, preferred_element_type=preferred_element_type)
  return lax_internal._convert_element_type(result, preferred_element_type, output_weak_type)
