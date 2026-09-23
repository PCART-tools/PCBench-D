def einsum(
    subscripts, /,
    *operands,
    out: None = None,
    optimize: str | bool | list[tuple[int, ...]] = "optimal",
    precision: PrecisionLike = None,
    preferred_element_type: DTypeLike | None = None,
    _dot_general: Callable[..., Array] = lax.dot_general,
) -> Array:
  """Einstein summation

  JAX implementation of :func:`numpy.einsum`.

  ``einsum`` is a powerful and generic API for computing various reductions,
  inner products, outer products, axis reorderings, and combinations thereof
  across one or more input arrays. It has a somewhat complicated overloaded API;
  the arguments below reflect the most common calling convention. The Examples
  section below demonstrates some of the alternative calling conventions.

  Args:
    subscripts: string containing axes names separated by commas.
    *operands: sequence of one or more arrays corresponding to the subscripts.
    optimize: specify how to optimize the order of computation. In JAX this defaults
      to ``"optimal"`` which produces optimized expressions via the opt_einsum_
      package. Other options are ``True`` (same as ``"optimal"``), ``False``
      (unoptimized), or any string supported by ``opt_einsum``, which
      includes ``"auto"``, ``"greedy"``, ``"eager"``, and others. It may also
      be a pre-computed path (see :func:`~jax.numpy.einsum_path`).
    precision: either ``None`` (default), which means the default precision for
      the backend, a :class:`~jax.lax.Precision` enum value (``Precision.DEFAULT``,
      ``Precision.HIGH`` or ``Precision.HIGHEST``).
    preferred_element_type: either ``None`` (default), which means the default
      accumulation type for the input types, or a datatype, indicating to
      accumulate results to and return a result with that datatype.
    out: unsupported by JAX
    _dot_general: optionally override the ``dot_general`` callable used by ``einsum``.
      This parameter is experimental, and may be removed without warning at any time.

  Returns:
    array containing the result of the einstein summation.

  See also:
    :func:`jax.numpy.einsum_path`

  Examples:
    The mechanics of ``einsum`` are perhaps best demonstrated by example. Here we
    show how to use ``einsum`` to compute a number of quantities from one or more
    arrays. For more discussion and examples of ``einsum``, see the documentation
    of :func:`numpy.einsum`.

    >>> M = jnp.arange(16).reshape(4, 4)
    >>> x = jnp.arange(4)
    >>> y = jnp.array([5, 4, 3, 2])

    **Vector product**

    >>> jnp.einsum('i,i', x, y)
    Array(16, dtype=int32)
    >>> jnp.vecdot(x, y)
    Array(16, dtype=int32)

    Here are some alternative ``einsum`` calling conventions to compute the same
    result:

    >>> jnp.einsum('i,i->', x, y)  # explicit form
    Array(16, dtype=int32)
    >>> jnp.einsum(x, (0,), y, (0,))  # implicit form via indices
    Array(16, dtype=int32)
    >>> jnp.einsum(x, (0,), y, (0,), ())  # explicit form via indices
    Array(16, dtype=int32)

    **Matrix product**

    >>> jnp.einsum('ij,j->i', M, x)  # explicit form
    Array([14, 38, 62, 86], dtype=int32)
    >>> jnp.matmul(M, x)
    Array([14, 38, 62, 86], dtype=int32)

    Here are some alternative ``einsum`` calling conventions to compute the same
    result:

    >>> jnp.einsum('ij,j', M, x) # implicit form
    Array([14, 38, 62, 86], dtype=int32)
    >>> jnp.einsum(M, (0, 1), x, (1,), (0,)) # explicit form via indices
    Array([14, 38, 62, 86], dtype=int32)
    >>> jnp.einsum(M, (0, 1), x, (1,))  # implicit form via indices
    Array([14, 38, 62, 86], dtype=int32)

    **Outer product**

    >>> jnp.einsum("i,j->ij", x, y)
    Array([[ 0,  0,  0,  0],
           [ 5,  4,  3,  2],
           [10,  8,  6,  4],
           [15, 12,  9,  6]], dtype=int32)
    >>> jnp.outer(x, y)
    Array([[ 0,  0,  0,  0],
           [ 5,  4,  3,  2],
           [10,  8,  6,  4],
           [15, 12,  9,  6]], dtype=int32)

    Some other ways of computing outer products:

    >>> jnp.einsum("i,j", x, y)  # implicit form
    Array([[ 0,  0,  0,  0],
           [ 5,  4,  3,  2],
           [10,  8,  6,  4],
           [15, 12,  9,  6]], dtype=int32)
    >>> jnp.einsum(x, (0,), y, (1,), (0, 1))  # explicit form via indices
    Array([[ 0,  0,  0,  0],
           [ 5,  4,  3,  2],
           [10,  8,  6,  4],
           [15, 12,  9,  6]], dtype=int32)
    >>> jnp.einsum(x, (0,), y, (1,))  # implicit form via indices
    Array([[ 0,  0,  0,  0],
           [ 5,  4,  3,  2],
           [10,  8,  6,  4],
           [15, 12,  9,  6]], dtype=int32)

    **1D array sum**

    >>> jnp.einsum("i->", x)  # requires explicit form
    Array(6, dtype=int32)
    >>> jnp.einsum(x, (0,), ())  # explicit form via indices
    Array(6, dtype=int32)
    >>> jnp.sum(x)
    Array(6, dtype=int32)

    **Sum along an axis**

    >>> jnp.einsum("...j->...", M)  # requires explicit form
    Array([ 6, 22, 38, 54], dtype=int32)
    >>> jnp.einsum(M, (..., 0), (...,))  # explicit form via indices
    Array([ 6, 22, 38, 54], dtype=int32)
    >>> M.sum(-1)
    Array([ 6, 22, 38, 54], dtype=int32)

    **Matrix transpose**

    >>> y = jnp.array([[1, 2, 3],
    ...                [4, 5, 6]])
    >>> jnp.einsum("ij->ji", y)  # explicit form
    Array([[1, 4],
           [2, 5],
           [3, 6]], dtype=int32)
    >>> jnp.einsum("ji", y)  # implicit form
    Array([[1, 4],
           [2, 5],
           [3, 6]], dtype=int32)
    >>> jnp.einsum(y, (1, 0))  # implicit form via indices
    Array([[1, 4],
           [2, 5],
           [3, 6]], dtype=int32)
    >>> jnp.einsum(y, (0, 1), (1, 0))  # explicit form via indices
    Array([[1, 4],
           [2, 5],
           [3, 6]], dtype=int32)
    >>> jnp.transpose(y)
    Array([[1, 4],
           [2, 5],
           [3, 6]], dtype=int32)

    **Matrix diagonal**

    >>> jnp.einsum("ii->i", M)
    Array([ 0,  5, 10, 15], dtype=int32)
    >>> jnp.diagonal(M)
    Array([ 0,  5, 10, 15], dtype=int32)

    **Matrix trace**

    >>> jnp.einsum("ii", M)
    Array(30, dtype=int32)
    >>> jnp.trace(M)
    Array(30, dtype=int32)

    **Tensor products**

    >>> x = jnp.arange(30).reshape(2, 3, 5)
    >>> y = jnp.arange(60).reshape(3, 4, 5)
    >>> jnp.einsum('ijk,jlk->il', x, y)  # explicit form
    Array([[ 3340,  3865,  4390,  4915],
           [ 8290,  9940, 11590, 13240]], dtype=int32)
    >>> jnp.tensordot(x, y, axes=[(1, 2), (0, 2)])
    Array([[ 3340,  3865,  4390,  4915],
           [ 8290,  9940, 11590, 13240]], dtype=int32)
    >>> jnp.einsum('ijk,jlk', x, y)  # implicit form
    Array([[ 3340,  3865,  4390,  4915],
           [ 8290,  9940, 11590, 13240]], dtype=int32)
    >>> jnp.einsum(x, (0, 1, 2), y, (1, 3, 2), (0, 3))  # explicit form via indices
    Array([[ 3340,  3865,  4390,  4915],
           [ 8290,  9940, 11590, 13240]], dtype=int32)
    >>> jnp.einsum(x, (0, 1, 2), y, (1, 3, 2))  # implicit form via indices
    Array([[ 3340,  3865,  4390,  4915],
           [ 8290,  9940, 11590, 13240]], dtype=int32)

    **Chained dot products**

    >>> w = jnp.arange(5, 9).reshape(2, 2)
    >>> x = jnp.arange(6).reshape(2, 3)
    >>> y = jnp.arange(-2, 4).reshape(3, 2)
    >>> z = jnp.array([[2, 4, 6], [3, 5, 7]])
    >>> jnp.einsum('ij,jk,kl,lm->im', w, x, y, z)
    Array([[ 481,  831, 1181],
           [ 651, 1125, 1599]], dtype=int32)
    >>> jnp.einsum(w, (0, 1), x, (1, 2), y, (2, 3), z, (3, 4))  # implicit, via indices
    Array([[ 481,  831, 1181],
           [ 651, 1125, 1599]], dtype=int32)
    >>> w @ x @ y @ z  # direct chain of matmuls
    Array([[ 481,  831, 1181],
           [ 651, 1125, 1599]], dtype=int32)
    >>> jnp.linalg.multi_dot([w, x, y, z])
    Array([[ 481,  831, 1181],
           [ 651, 1125, 1599]], dtype=int32)

  .. _opt_einsum: https://github.com/dgasmith/opt_einsum
  """
  operands = (subscripts, *operands)
  if out is not None:
    raise NotImplementedError("The 'out' argument to jnp.einsum is not supported.")
  spec = operands[0] if isinstance(operands[0], str) else None
  path_type = 'optimal' if optimize is True else Unoptimized() if optimize is False else optimize

  # Allow handling of shape polymorphism
  non_constant_dim_types = {
      type(d) for op in operands if not isinstance(op, str)
      for d in np.shape(op) if not core.is_constant_dim(d)
  }
  if not non_constant_dim_types:
    contract_path = opt_einsum.contract_path
  else:
    ty = next(iter(non_constant_dim_types))
    contract_path = _poly_einsum_handlers.get(ty, _default_poly_einsum_handler)
  # using einsum_call=True here is an internal api for opt_einsum... sorry
  operands, contractions = contract_path(
        *operands, einsum_call=True, use_blas=True, optimize=path_type)

  contractions = tuple((a, frozenset(b), c) for a, b, c, *_ in contractions)

  einsum = jit(_einsum, static_argnums=(1, 2, 3, 4), inline=True)
  if spec is not None:
    einsum = jax.named_call(einsum, name=spec)
  return einsum(operands, contractions, precision,
                preferred_element_type, _dot_general)
