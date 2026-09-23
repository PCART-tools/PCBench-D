def multi_dot(arrays: Sequence[ArrayLike], *, precision: PrecisionLike = None) -> Array:
  """Efficiently compute matrix products between a sequence of arrays.

  JAX implementation of :func:`numpy.linalg.multi_dot`.

  JAX internally uses the opt_einsum library to compute the most efficient
  operation order.

  Args:
    arrays: sequence of arrays. All must be two-dimensional, except the first
      and last which may be one-dimensional.
    precision: either ``None`` (default), which means the default precision for
      the backend, a :class:`~jax.lax.Precision` enum value (``Precision.DEFAULT``,
      ``Precision.HIGH`` or ``Precision.HIGHEST``).

  Returns:
    an array representing the equivalent of ``reduce(jnp.matmul, arrays)``, but
    evaluated in the optimal order.

  This function exists because the cost of computing sequences of matmul operations
  can differ vastly depending on the order in which the operations are evaluated.
  For a single matmul, the number of floating point operations (flops) required to
  compute a matrix product can be approximated this way:

  >>> def approx_flops(x, y):
  ...   # for 2D x and y, with x.shape[1] == y.shape[0]
  ...   return 2 * x.shape[0] * x.shape[1] * y.shape[1]

  Suppose we have three matrices that we'd like to multiply in sequence:

  >>> key1, key2, key3 = jax.random.split(jax.random.key(0), 3)
  >>> x = jax.random.normal(key1, shape=(200, 5))
  >>> y = jax.random.normal(key2, shape=(5, 100))
  >>> z = jax.random.normal(key3, shape=(100, 10))

  Because of associativity of matrix products, there are two orders in which we might
  evaluate the product ``x @ y @ z``, and both produce equivalent outputs up to floating
  point precision:

  >>> result1 = (x @ y) @ z
  >>> result2 = x @ (y @ z)
  >>> jnp.allclose(result1, result2, atol=1E-4)
  Array(True, dtype=bool)

  But the computational cost of these differ greatly:

  >>> print("(x @ y) @ z flops:", approx_flops(x, y) + approx_flops(x @ y, z))
  (x @ y) @ z flops: 600000
  >>> print("x @ (y @ z) flops:", approx_flops(y, z) + approx_flops(x, y @ z))
  x @ (y @ z) flops: 30000

  The second approach is about 20x more efficient in terms of estimated flops!

  ``multi_dot`` is a function that will automatically choose the fastest
  computational path for such problems:

  >>> result3 = jnp.linalg.multi_dot([x, y, z])
  >>> jnp.allclose(result1, result3, atol=1E-4)
  Array(True, dtype=bool)

  We can use JAX's :ref:`ahead-of-time-lowering` tools to estimate the total flops
  of each approach, and confirm that ``multi_dot`` is choosing the more efficient
  option:

  >>> jax.jit(lambda x, y, z: (x @ y) @ z).lower(x, y, z).cost_analysis()['flops']
  600000.0
  >>> jax.jit(lambda x, y, z: x @ (y @ z)).lower(x, y, z).cost_analysis()['flops']
  30000.0
  >>> jax.jit(jnp.linalg.multi_dot).lower([x, y, z]).cost_analysis()['flops']
  30000.0
  """
  check_arraylike('jnp.linalg.multi_dot', *arrays)
  arrs: list[Array] = list(map(jnp.asarray, arrays))
  if len(arrs) < 2:
    raise ValueError(f"multi_dot requires at least two arrays; got len(arrays)={len(arrs)}")
  if not (arrs[0].ndim in (1, 2) and arrs[-1].ndim in (1, 2) and
          all(a.ndim == 2 for a in arrs[1:-1])):
    raise ValueError("multi_dot: input arrays must all be two-dimensional, except for"
                     " the first and last array which may be 1 or 2 dimensional."
                     f" Got array shapes {[a.shape for a in arrs]}")
  if any(a.shape[-1] != b.shape[0] for a, b in zip(arrs[:-1], arrs[1:])):
    raise ValueError("multi_dot: last dimension of each array must match first dimension"
                     f" of following array. Got array shapes {[a.shape for a in arrs]}")
  einsum_axes: list[tuple[int, ...]] = [(i, i+1) for i in range(len(arrs))]
  if arrs[0].ndim == 1:
    einsum_axes[0] = einsum_axes[0][1:]
  if arrs[-1].ndim == 1:
    einsum_axes[-1] = einsum_axes[-1][:1]
  return jnp.einsum(*itertools.chain(*zip(arrs, einsum_axes)),  # type: ignore[call-overload]
                    optimize='optimal', precision=precision)
