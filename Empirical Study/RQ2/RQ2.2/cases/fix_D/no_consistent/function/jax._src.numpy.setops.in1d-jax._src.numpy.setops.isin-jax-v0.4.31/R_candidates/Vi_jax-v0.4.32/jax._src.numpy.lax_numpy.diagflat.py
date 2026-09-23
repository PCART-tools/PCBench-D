def diagflat(v: ArrayLike, k: int = 0) -> Array:
  """Return a 2-D array with the flattened input array laid out on the diagonal.

  JAX implementation of :func:`numpy.diagflat`.

  This differs from `np.diagflat` for some scalar values of `v`. JAX always returns
  a two-dimensional array, whereas NumPy may return a scalar depending on the type
  of `v`.

  Args:
    v: Input array. Can be N-dimensional but is flattened to 1D.
    k: optional, default=0. Diagonal offset. Positive values place the diagonal
      above the main diagonal, negative values place it below the main diagonal.

  Returns:
    A 2D array with the input elements placed along the diagonal with the
    specified offset (k). The remaining entries are filled with zeros.

  See also:
    - :func:`jax.numpy.diag`
    - :func:`jax.numpy.diagonal`

  Examples:
    >>> jnp.diagflat(jnp.array([1, 2, 3]))
    Array([[1, 0, 0],
           [0, 2, 0],
           [0, 0, 3]], dtype=int32)
    >>> jnp.diagflat(jnp.array([1, 2, 3]), k=1)
    Array([[0, 1, 0, 0],
           [0, 0, 2, 0],
           [0, 0, 0, 3],
           [0, 0, 0, 0]], dtype=int32)
    >>> a = jnp.array([[1, 2],
    ...                [3, 4]])
    >>> jnp.diagflat(a)
    Array([[1, 0, 0, 0],
           [0, 2, 0, 0],
           [0, 0, 3, 0],
           [0, 0, 0, 4]], dtype=int32)
  """
  util.check_arraylike("diagflat", v)
  v_ravel = ravel(v)
  v_length = len(v_ravel)
  adj_length = v_length + abs(k)
  res = zeros(adj_length*adj_length, dtype=v_ravel.dtype)
  i = arange(0, adj_length-abs(k))
  if (k >= 0):
    fi = i+k+i*adj_length
  else:
    fi = i+(i-k)*adj_length
  res = res.at[fi].set(v_ravel)
  res = res.reshape(adj_length, adj_length)
  return res
