class _Mgrid:
  """Return dense multi-dimensional "meshgrid".

  LAX-backend implementation of :obj:`numpy.mgrid`. This is a convenience wrapper for
  functionality provided by :func:`jax.numpy.meshgrid` with ``sparse=False``.

  See Also:
    jnp.ogrid: open/sparse version of jnp.mgrid

  Examples:
    Pass ``[start:stop:step]`` to generate values similar to :func:`jax.numpy.arange`:

    >>> jnp.mgrid[0:4:1]
    Array([0, 1, 2, 3], dtype=int32)

    Passing an imaginary step generates values similar to :func:`jax.numpy.linspace`:

    >>> jnp.mgrid[0:1:4j]
    Array([0.        , 0.33333334, 0.6666667 , 1.        ], dtype=float32)

    Multiple slices can be used to create broadcasted grids of indices:

    >>> jnp.mgrid[:2, :3]
    Array([[[0, 0, 0],
            [1, 1, 1]],
           [[0, 1, 2],
            [0, 1, 2]]], dtype=int32)
  """

  def __getitem__(self, key: slice | tuple[slice, ...]) -> Array:
    if isinstance(key, slice):
      return _make_1d_grid_from_slice(key, op_name="mgrid")
    output: Iterable[Array] = (_make_1d_grid_from_slice(k, op_name="mgrid") for k in key)
    with jax.numpy_dtype_promotion('standard'):
      output = promote_dtypes(*output)
    output_arr = meshgrid(*output, indexing='ij', sparse=False)
    if len(output_arr) == 0:
      return arange(0)
    return stack(output_arr, 0)
