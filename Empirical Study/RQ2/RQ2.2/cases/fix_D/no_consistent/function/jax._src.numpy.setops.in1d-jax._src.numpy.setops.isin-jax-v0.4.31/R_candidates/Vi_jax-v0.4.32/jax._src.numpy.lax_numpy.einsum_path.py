def einsum_path(
    subscripts, /,
    *operands,
    optimize: bool | str | list[tuple[int, ...]] = 'auto'
  ) -> tuple[list[tuple[int, ...]], Any]:
  """Evaluates the optimal contraction path without evaluating the einsum.

  JAX implementation of :func:`numpy.einsum_path`. This function calls into
  the opt_einsum_ package, and makes use of its optimization routines.

  Args:
    subscripts: string containing axes names separated by commas.
    *operands: sequence of one or more arrays corresponding to the subscripts.
    optimize: specify how to optimize the order of computation. In JAX this defaults
      to ``"auto"``. Other options are ``True`` (same as ``"optimize"``), ``False``
      (unoptimized), or any string supported by ``opt_einsum``, which
      includes ``"optimize"``,, ``"greedy"``, ``"eager"``, and others.

  Returns:
    A tuple containing the path that may be passed to :func:`~jax.numpy.einsum`, and a
    printable object representing this optimal path.

  Examples:
    >>> key1, key2, key3 = jax.random.split(jax.random.key(0), 3)
    >>> x = jax.random.randint(key1, minval=-5, maxval=5, shape=(2, 3))
    >>> y = jax.random.randint(key2, minval=-5, maxval=5, shape=(3, 100))
    >>> z = jax.random.randint(key3, minval=-5, maxval=5, shape=(100, 5))
    >>> path, path_info = jnp.einsum_path("ij,jk,kl", x, y, z, optimize="optimal")
    >>> print(path)
    [(1, 2), (0, 1)]
    >>> print(path_info)
          Complete contraction:  ij,jk,kl->il
                Naive scaling:  4
            Optimized scaling:  3
              Naive FLOP count:  9.000e+3
          Optimized FLOP count:  3.060e+3
          Theoretical speedup:  2.941e+0
          Largest intermediate:  1.500e+1 elements
        --------------------------------------------------------------------------------
        scaling        BLAS                current                             remaining
        --------------------------------------------------------------------------------
          3           GEMM              kl,jk->lj                             ij,lj->il
          3           GEMM              lj,ij->il                                il->il

    Use the computed path in :func:`~jax.numpy.einsum`:

    >>> jnp.einsum("ij,jk,kl", x, y, z, optimize=path)
    Array([[-539,  216,   95,  592,  209],
           [ 527,   76,  285, -436, -529]], dtype=int32)

  .. _opt_einsum: https://github.com/dgasmith/opt_einsum
  """
  if optimize is True:
    optimize = 'optimal'
  elif optimize is False:
    optimize = Unoptimized()
  return opt_einsum.contract_path(subscripts, *operands, optimize=optimize)
