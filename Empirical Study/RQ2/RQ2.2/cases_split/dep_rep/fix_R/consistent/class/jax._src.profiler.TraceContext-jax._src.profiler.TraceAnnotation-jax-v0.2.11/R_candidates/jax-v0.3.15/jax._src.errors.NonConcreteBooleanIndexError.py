class NonConcreteBooleanIndexError(JAXIndexError):
  """
  This error occurs when a program attempts to use non-concrete boolean indices
  in a traced indexing operation. Under JIT compilation, JAX arrays must have
  static shapes (i.e. shapes that are known at compile-time) and so boolean
  masks must be used carefully. Some logic implemented via boolean masking is
  simply not possible in a :func:`jax.jit` function; in other cases, the logic
  can be re-expressed in a JIT-compatible way, often using the three-argument
  version of :func:`~jax.numpy.where`.

  Following are a few examples of when this error might arise.

  Constructing arrays via boolean masking
    This most commonly arises when attempting to create an array via a boolean
    mask within a JIT context. For example::

      >>> import jax
      >>> import jax.numpy as jnp

      >>> @jax.jit
      ... def positive_values(x):
      ...   return x[x > 0]

      >>> positive_values(jnp.arange(-5, 5))  # doctest: +IGNORE_EXCEPTION_DETAIL
      Traceback (most recent call last):
          ...
      NonConcreteBooleanIndexError: Array boolean indices must be concrete: ShapedArray(bool[10])

    This function is attempting to return only the positive values in the input
    array; the size of this returned array cannot be determined at compile-time
    unless `x` is marked as static, and so operations like this cannot be
    performed under JIT compilation.

  Reexpressible Boolean Logic
    Although creating dynamically sized arrays is not supported directly, in
    many cases it is possible to re-express the logic of the computation in
    terms of a JIT-compatible operation. For example, here is another function
    that fails under JIT for the same reason::

      >>> @jax.jit
      ... def sum_of_positive(x):
      ...   return x[x > 0].sum()

      >>> sum_of_positive(jnp.arange(-5, 5))  # doctest: +IGNORE_EXCEPTION_DETAIL
      Traceback (most recent call last):
          ...
      NonConcreteBooleanIndexError: Array boolean indices must be concrete: ShapedArray(bool[10])

    In this case, however, the problematic array is only an intermediate value,
    and we can instead express the same logic in terms of the JIT-compatible
    three-argument version of :func:`jax.numpy.where`::

      >>> @jax.jit
      ... def sum_of_positive(x):
      ...   return jnp.where(x > 0, x, 0).sum()

      >>> sum_of_positive(jnp.arange(-5, 5))
      DeviceArray(10, dtype=int32)

    This pattern of replacing boolean masking with three-argument
    :func:`~jax.numpy.where` is a common solution to this sort of problem.

  Boolean indexing into JAX arrays
    The other situation where this error often arises is when using boolean
    indices, such as with :code:`.at[...].set(...)`. Here is a simple example::

      >>> @jax.jit
      ... def manual_clip(x):
      ...   return x.at[x < 0].set(0)

      >>> manual_clip(jnp.arange(-2, 2))  # doctest: +IGNORE_EXCEPTION_DETAIL
      Traceback (most recent call last):
          ...
      NonConcreteBooleanIndexError: Array boolean indices must be concrete: ShapedArray(bool[4])

    This function is attempting to set values smaller than zero to a scalar fill
    value. As above, this can be addressed by re-expressing the logic in terms
    of :func:`~jax.numpy.where`::

      >>> @jax.jit
      ... def manual_clip(x):
      ...   return jnp.where(x < 0, 0, x)

      >>> manual_clip(jnp.arange(-2, 2))
      DeviceArray([0, 0, 0, 1], dtype=int32)
  """
  def __init__(self, tracer: "core.Tracer"):
    super().__init__(
        f"Array boolean indices must be concrete; got {tracer}\n")
