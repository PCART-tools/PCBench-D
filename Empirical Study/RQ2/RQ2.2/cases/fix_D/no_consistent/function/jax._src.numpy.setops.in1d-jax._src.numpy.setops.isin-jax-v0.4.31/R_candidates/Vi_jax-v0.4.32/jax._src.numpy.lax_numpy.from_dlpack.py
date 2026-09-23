def from_dlpack(x: Any, /, *, device: xc.Device | Sharding | None = None,
                copy: bool | None = None) -> Array:
  """Construct a JAX array via DLPack.

  JAX implementation of :func:`numpy.from_dlpack`.

  Args:
    x: An object that implements the DLPack_ protocol via the ``__dlpack__``
      and ``__dlpack_device__`` methods, or a legacy DLPack tensor on either
      CPU or GPU.
    device: An optional :class:`~jax.Device` or :class:`~jax.sharding.Sharding`,
      representing the single device onto which the returned array should be placed.
      If given, then the result is committed to the device. If unspecified,
      the resulting array will be unpacked onto the same device it originated from.
      Setting ``device`` to a device different from the source of ``external_array``
      will require a copy, meaning ``copy`` must be set to either ``True`` or ``None``.
    copy: An optional boolean, controlling whether or not a copy is performed.
      If ``copy=True`` then a copy is always performed, even if unpacked onto the
      same device. If ``copy=False`` then the copy is never performed and will raise
      an error if necessary. When ``copy=None`` (default) then a copy may be performed
      if needed for a device transfer.

  Returns:
    A JAX array of the imput buffer.

  Note:
    While JAX arrays are always immutable, dlpack buffers cannot be marked as
    immutable, and it is possible for processes external to JAX to mutate them
    in-place. If a JAX Array is constructed from a dlpack buffer without copying
    and the source buffer is later modified in-place, it may lead to undefined
    behavior when using the associated JAX array.

  Examples:
    Passing data between NumPy and JAX via DLPack_:

    >>> import numpy as np
    >>> rng = np.random.default_rng(42)
    >>> x_numpy = rng.random(4, dtype='float32')
    >>> print(x_numpy)
    [0.08925092 0.773956   0.6545715  0.43887842]
    >>> hasattr(x_numpy, "__dlpack__")  # NumPy supports the DLPack interface
    True

    >>> import jax.numpy as jnp
    >>> x_jax = jnp.from_dlpack(x_numpy)
    >>> print(x_jax)
    [0.08925092 0.773956   0.6545715  0.43887842]
    >>> hasattr(x_jax, "__dlpack__")  # JAX supports the DLPack interface
    True

    >>> x_numpy_round_trip = np.from_dlpack(x_jax)
    >>> print(x_numpy_round_trip)
    [0.08925092 0.773956   0.6545715  0.43887842]

  .. _DLPack: https://dmlc.github.io/dlpack
  """
  from jax.dlpack import from_dlpack  # pylint: disable=g-import-not-at-top
  return from_dlpack(x, device=device, copy=copy)
