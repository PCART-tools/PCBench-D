def arange(start: ArrayLike | DimSize, stop: ArrayLike | DimSize | None = None,
           step: ArrayLike | None = None, dtype: DTypeLike | None = None,
           *, device: xc.Device | Sharding | None = None) -> Array:
  """Create an array of evenly-spaced values.

  JAX implementation of :func:`numpy.arange`, implemented in terms of
  :func:`jax.lax.iota`.

  Similar to Python's :func:`range` function, this can be called with a few
  different positional signatures:

  - ``jnp.arange(stop)``: generate values from 0 to ``stop``, stepping by 1.
  - ``jnp.arange(start, stop)``: generate values from ``start`` to ``stop``,
    stepping by 1.
  - ``jnp.arange(start, stop, step)``: generate values from ``start`` to ``stop``,
    stepping by ``step``.

  Like with Python's :func:`range` function, the starting value is inclusive,
  and the stop value is exclusive.

  Args:
    start: start of the interval, inclusive.
    stop: optional end of the interval, exclusive. If not specified, then
      ``(start, stop) = (0, start)``
    step: optional step size for the interval. Default = 1.
    dtype: optional dtype for the returned array; if not specified it will
      be determined via type promotion of `start`, `stop`, and `step`.
    device: (optional) :class:`~jax.Device` or :class:`~jax.sharding.Sharding`
      to which the created array will be committed.

  Returns:
    Array of evenly-spaced values from ``start`` to ``stop``, separated by ``step``.

  Note:
    Using ``arange`` with a floating-point ``step`` argument can lead to unexpected
    results due to accumulation of floating-point errors, especially with
    lower-precision data types like ``float8_*`` and ``bfloat16``.
    To avoid precision errors, consider generating a range of integers, and scaling
    it to the desired range. For example, instead of this::

       jnp.arange(-1, 1, 0.01, dtype='bfloat16')

    it can be more accurate to generate a sequence of integers, and scale them::

       (jnp.arange(-100, 100) * 0.01).astype('bfloat16')

  Examples:
    Single-argument version specifies only the ``stop`` value:

    >>> jnp.arange(4)
    Array([0, 1, 2, 3], dtype=int32)

    Passing a floating-point ``stop`` value leads to a floating-point result:

    >>> jnp.arange(4.0)
    Array([0., 1., 2., 3.], dtype=float32)

    Two-argument version specifies ``start`` and ``stop``, with ``step=1``:

    >>> jnp.arange(1, 6)
    Array([1, 2, 3, 4, 5], dtype=int32)

    Three-argument version specifies ``start``, ``stop``, and ``step``:

    >>> jnp.arange(0, 2, 0.5)
    Array([0. , 0.5, 1. , 1.5], dtype=float32)

  See Also:
    - :func:`jax.numpy.linspace`: generate a fixed number of evenly-spaced values.
    - :func:`jax.lax.iota`: directly generate integer sequences in XLA.
  """
  # TODO(vfdev-5): optimize putting the array directly on the device specified
  # instead of putting it on default device and then on the specific device
  output = _arange(start, stop=stop, step=step, dtype=dtype)
  if device is not None:
    return jax.device_put(output, device=device)
  return output
