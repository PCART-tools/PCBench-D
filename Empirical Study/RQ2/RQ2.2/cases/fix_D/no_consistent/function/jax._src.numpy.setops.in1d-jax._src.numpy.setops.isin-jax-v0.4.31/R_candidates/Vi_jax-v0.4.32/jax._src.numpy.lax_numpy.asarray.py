def asarray(a: Any, dtype: DTypeLike | None = None, order: str | None = None,
            *, copy: bool | None = None,
            device: xc.Device | Sharding | None = None) -> Array:
  """Convert an object to a JAX array.

  JAX implementation of :func:`numpy.asarray`.

  Args:
    a: an object that is convertible to an array. This includes JAX
      arrays, NumPy arrays, Python scalars, Python collections like lists
      and tuples, objects with an ``__array__`` method, and objects
      supporting the Python buffer protocol.
    dtype: optionally specify the dtype of the output array. If not
      specified it will be inferred from the input.
    order: not implemented in JAX
    copy: optional boolean specifying the copy mode. If True, then always
      return a copy. If False, then error if a copy is necessary. Default is
      None, which will only copy when necessary.
    device: optional :class:`~jax.Device` or :class:`~jax.sharding.Sharding`
      to which the created array will be committed.

  Returns:
    A JAX array constructed from the input.

  See also:
    - :func:`jax.numpy.array`: like `asarray`, but defaults to `copy=True`.
    - :func:`jax.numpy.from_dlpack`: construct a JAX array from an object
      that implements the dlpack interface.
    - :func:`jax.numpy.frombuffer`: construct a JAX array from an object
      that implements the buffer interface.

  Examples:
    Constructing JAX arrays from Python scalars:

    >>> jnp.asarray(True)
    Array(True, dtype=bool)
    >>> jnp.asarray(42)
    Array(42, dtype=int32, weak_type=True)
    >>> jnp.asarray(3.5)
    Array(3.5, dtype=float32, weak_type=True)
    >>> jnp.asarray(1 + 1j)
    Array(1.+1.j, dtype=complex64, weak_type=True)

    Constructing JAX arrays from Python collections:

    >>> jnp.asarray([1, 2, 3])  # list of ints -> 1D array
    Array([1, 2, 3], dtype=int32)
    >>> jnp.asarray([(1, 2, 3), (4, 5, 6)])  # list of tuples of ints -> 2D array
    Array([[1, 2, 3],
           [4, 5, 6]], dtype=int32)
    >>> jnp.asarray(range(5))
    Array([0, 1, 2, 3, 4], dtype=int32)

    Constructing JAX arrays from NumPy arrays:

    >>> jnp.asarray(np.linspace(0, 2, 5))
    Array([0. , 0.5, 1. , 1.5, 2. ], dtype=float32)

    Constructing a JAX array via the Python buffer interface, using Python's
    built-in :mod:`array` module.

    >>> from array import array
    >>> pybuffer = array('i', [2, 3, 5, 7])
    >>> jnp.asarray(pybuffer)
    Array([2, 3, 5, 7], dtype=int32)
  """
  # For copy=False, the array API specifies that we raise a ValueError if the input supports
  # the buffer protocol but a copy is required. Since array() supports the buffer protocol
  # via numpy, this is only the case when the default device is not 'cpu'
  if (copy is False and not isinstance(a, Array)
      and jax.default_backend() != 'cpu'
      and _supports_buffer_protocol(a)):
    raise ValueError(f"jnp.asarray: cannot convert object of type {type(a)} to JAX Array "
                     f"on backend={jax.default_backend()!r} with copy=False. "
                      "Consider using copy=None or copy=True instead.")
  dtypes.check_user_dtype_supported(dtype, "asarray")
  if dtype is not None:
    dtype = dtypes.canonicalize_dtype(dtype, allow_extended_dtype=True)  # type: ignore[assignment]
  return array(a, dtype=dtype, copy=bool(copy), order=order, device=device)
