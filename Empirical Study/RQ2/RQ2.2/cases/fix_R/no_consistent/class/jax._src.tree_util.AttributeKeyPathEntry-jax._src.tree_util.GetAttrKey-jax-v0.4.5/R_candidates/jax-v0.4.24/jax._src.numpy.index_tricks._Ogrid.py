class _Ogrid:
  """Return open multi-dimensional "meshgrid".

  LAX-backend implementation of :obj:`numpy.ogrid`. This is a convenience wrapper for
  functionality provided by :func:`jax.numpy.meshgrid` with ``sparse=True``.

  See Also:
    jnp.mgrid: dense version of jnp.ogrid

  Examples:
    Pass ``[start:stop:step]`` to generate values similar to :func:`jax.numpy.arange`:

    >>> jnp.ogrid[0:4:1]
    Array([0, 1, 2, 3], dtype=int32)

    Passing an imaginary step generates values similar to :func:`jax.numpy.linspace`:

    >>> jnp.ogrid[0:1:4j]
    Array([0.        , 0.33333334, 0.6666667 , 1.        ], dtype=float32)

    Multiple slices can be used to create sparse grids of indices:

    >>> jnp.ogrid[:2, :3]
    [Array([[0],
            [1]], dtype=int32),
     Array([[0, 1, 2]], dtype=int32)]
  """

  def __getitem__(
      self, key: slice | tuple[slice, ...]
  ) -> Array | list[Array]:
    if isinstance(key, slice):
      return _make_1d_grid_from_slice(key, op_name="ogrid")
    output: Iterable[Array] = (_make_1d_grid_from_slice(k, op_name="ogrid") for k in key)
    with jax.numpy_dtype_promotion('standard'):
      output = promote_dtypes(*output)
    return meshgrid(*output, indexing='ij', sparse=True)
