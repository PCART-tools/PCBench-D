def linspace(start: ArrayLike, stop: ArrayLike, num: int = 50,
             endpoint: bool = True, retstep: bool = False,
             dtype: DTypeLike | None = None,
             axis: int = 0,
             *, device: xc.Device | Sharding | None = None) -> Array | tuple[Array, Array]:
  """Return evenly-spaced numbers within an interval.

  JAX implementation of :func:`numpy.linspace`.

  Args:
    start: scalar or array of starting values.
    stop: scalar or array of stop values.
    num: number of values to generate. Default: 50.
    endpoint: if True (default) then include the ``stop`` value in the result.
      If False, then exclude the ``stop`` value.
    retstep: If True, then return a ``(result, step)`` tuple, where ``step`` is the
      interval between adjacent values in ``result``.
    axis: integer axis along which to generate the linspace. Defaults to zero.
    device: optional :class:`~jax.Device` or :class:`~jax.sharding.Sharding`
      to which the created array will be committed.

  Returns:
    An array ``values``, or a tuple ``(values, step)`` if ``retstep`` is True, where:

    - ``values`` is an array of evenly-spaced values from ``start`` to ``stop``
    - ``step`` is the interval between adjacent values.

  See also:
    - :func:`jax.numpy.arange`: Generate ``N`` evenly-spaced values given a starting
      point and a step
    - :func:`jax.numpy.logspace`: Generate logarithmically-spaced values.
    - :func:`jax.numpy.geomspace`: Generate geometrically-spaced values.

  Examples:
    List of 5 values between 0 and 10:

    >>> jnp.linspace(0, 10, 5)
    Array([ 0. ,  2.5,  5. ,  7.5, 10. ], dtype=float32)

    List of 8 values between 0 and 10, excluding the endpoint:

    >>> jnp.linspace(0, 10, 8, endpoint=False)
    Array([0.  , 1.25, 2.5 , 3.75, 5.  , 6.25, 7.5 , 8.75], dtype=float32)

    List of values and the step size between them

    >>> vals, step = jnp.linspace(0, 10, 9, retstep=True)
    >>> vals
    Array([ 0.  ,  1.25,  2.5 ,  3.75,  5.  ,  6.25,  7.5 ,  8.75, 10.  ],      dtype=float32)
    >>> step
    Array(1.25, dtype=float32)

    Multi-dimensional linspace:

    >>> start = jnp.array([0, 5])
    >>> stop = jnp.array([5, 10])
    >>> jnp.linspace(start, stop, 5)
    Array([[ 0.  ,  5.  ],
           [ 1.25,  6.25],
           [ 2.5 ,  7.5 ],
           [ 3.75,  8.75],
           [ 5.  , 10.  ]], dtype=float32)
  """
  num = core.concrete_dim_or_error(num, "'num' argument of jnp.linspace")
  axis = core.concrete_or_error(operator.index, axis, "'axis' argument of jnp.linspace")
  return _linspace(start, stop, num, endpoint, retstep, dtype, axis, device=device)
