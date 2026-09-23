class _Ogrid(_IndexGrid):
  """Return open multi-dimensional "meshgrid".

  LAX-backend implementation of :obj:`numpy.ogrid`. This is a convenience wrapper for
  functionality provided by :func:`jax.numpy.meshgrid` with ``sparse=True``.

  See Also:
    jnp.mgrid: dense version of jnp.ogrid

  Examples:
    Pass ``[start:stop:step]`` to generate values similar to :func:`jax.numpy.arange`:

    >>> jnp.ogrid[0:4:1]
    DeviceArray([0, 1, 2, 3], dtype=int32)

    Passing an imaginary step generates values similar to :func:`jax.numpy.linspace`:

    >>> jnp.ogrid[0:1:4j]
    DeviceArray([0.        , 0.33333334, 0.6666667 , 1.        ], dtype=float32)

    Multiple slices can be used to create sparse grids of indices:

    >>> jnp.ogrid[:2, :3]
    [DeviceArray([[0],
                  [1]], dtype=int32),
     DeviceArray([[0, 1, 2]], dtype=int32)]
  """
  sparse = True
  op_name = "ogrid"
