@export
class ConcretizationTypeError(JAXTypeError):
  """
  This error occurs when a JAX Tracer object is used in a context where a
  concrete value is required (see :ref:`faq-different-kinds-of-jax-values`
  for more on what a Tracer is). In some situations, it can be easily fixed by
  marking problematic values as static; in others, it may indicate that your
  program is doing operations that are not directly supported by JAX's JIT
  compilation model.

  Examples:

  Traced value where static value is expected
    One common cause of this error is using a traced value where a static value
    is required. For example:

      >>> from functools import partial
      >>> from jax import jit
      >>> import jax.numpy as jnp
      >>> @jit
      ... def func(x, axis):
      ...   return x.min(axis)

      >>> func(jnp.arange(4), 0)  # doctest: +IGNORE_EXCEPTION_DETAIL
      Traceback (most recent call last):
          ...
      ConcretizationTypeError: Abstract tracer value encountered where concrete
      value is expected: axis argument to jnp.min().

    This can often be fixed by marking the problematic argument as static::

        >>> @partial(jit, static_argnums=1)
        ... def func(x, axis):
        ...   return x.min(axis)

        >>> func(jnp.arange(4), 0)
        Array(0, dtype=int32)

  Shape depends on Traced Value
    Such an error may also arise when a shape in your JIT-compiled computation
    depends on the values within a traced quantity. For example::

      >>> @jit
      ... def func(x):
      ...     return jnp.where(x < 0)

      >>> func(jnp.arange(4))  # doctest: +IGNORE_EXCEPTION_DETAIL
      Traceback (most recent call last):
          ...
      ConcretizationTypeError: Abstract tracer value encountered where concrete value is expected:
      The error arose in jnp.nonzero.

    This is an example of an operation that is incompatible with JAX's JIT
    compilation model, which requires array sizes to be known at compile-time.
    Here the size of the returned array depends on the contents of `x`, and such
    code cannot be JIT compiled.

    In many cases it is possible to work around this by modifying the logic used
    in the function; for example here is code with a similar issue::

      >>> @jit
      ... def func(x):
      ...     indices = jnp.where(x > 1)
      ...     return x[indices].sum()

      >>> func(jnp.arange(4))  # doctest: +IGNORE_EXCEPTION_DETAIL
      Traceback (most recent call last):
          ...
      ConcretizationTypeError: Abstract tracer value encountered where concrete
      value is expected: The error arose in jnp.nonzero.

    And here is how you might express the same operation in a way that avoids
    creation of a dynamically-sized index array::

      >>> @jit
      ... def func(x):
      ...   return jnp.where(x > 1, x, 0).sum()

      >>> func(jnp.arange(4))
      Array(5, dtype=int32)

  To understand more subtleties having to do with tracers vs. regular values,
  and concrete vs. abstract values, you may want to read
  :ref:`faq-different-kinds-of-jax-values`.
  """
  def __init__(self, tracer: core.Tracer, context: str = ""):
    super().__init__(
        "Abstract tracer value encountered where concrete value is expected: "
        f"{tracer._error_repr()}\n{context}{tracer._origin_msg()}\n")
