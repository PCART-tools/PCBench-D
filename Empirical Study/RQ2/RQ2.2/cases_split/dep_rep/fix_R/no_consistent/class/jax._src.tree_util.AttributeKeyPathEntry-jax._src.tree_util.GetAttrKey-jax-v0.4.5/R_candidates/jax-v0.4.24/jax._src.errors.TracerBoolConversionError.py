@export
class TracerBoolConversionError(ConcretizationTypeError):
  """
  This error occurs when a traced value in JAX is used in a context where a
  boolean value is expected (see :ref:`faq-different-kinds-of-jax-values`
  for more on what a Tracer is).

  The boolean cast may be an explicit (e.g. ``bool(x)``) or implicit, through use of
  control flow (e.g. ``if x > 0`` or ``while x``), use of Python boolean
  operators (e.g. ``z = x and y``, ``z = x or y``, ``z = not x``) or functions
  that use them (e.g. ``z = max(x, y)``, ``z = min(x, y)`` etc.).

  In some situations, this problem can be easily fixed by marking traced values as
  static; in others, it may indicate that your program is doing operations that are
  not directly supported by JAX's JIT compilation model.

  Examples:

  Traced value used in control flow
    One case where this often arises is when a traced value is used in
    Python control flow. For example::

      >>> from jax import jit
      >>> import jax.numpy as jnp
      >>> @jit
      ... def func(x, y):
      ...   return x if x.sum() < y.sum() else y

      >>> func(jnp.ones(4), jnp.zeros(4))  # doctest: +IGNORE_EXCEPTION_DETAIL
      Traceback (most recent call last):
          ...
      TracerBoolConversionError: Attempted boolean conversion of JAX Tracer [...]

    We could mark both inputs ``x`` and ``y`` as static, but that would defeat
    the purpose of using :func:`jax.jit` here. Another option is to re-express
    the if statement in terms of the three-term :func:`jax.numpy.where`::

      >>> @jit
      ... def func(x, y):
      ...   return jnp.where(x.sum() < y.sum(), x, y)

      >>> func(jnp.ones(4), jnp.zeros(4))
      Array([0., 0., 0., 0.], dtype=float32)

    For more complicated control flow including loops, see
    :ref:`lax-control-flow`.

  Control flow on traced values
    Another common cause of this error is if you inadvertently trace over a boolean
    flag. For example::

      >>> @jit
      ... def func(x, normalize=True):
      ...   if normalize:
      ...     return x / x.sum()
      ...   return x

      >>> func(jnp.arange(5), True)  # doctest: +IGNORE_EXCEPTION_DETAIL
      Traceback (most recent call last):
          ...
      TracerBoolConversionError: Attempted boolean conversion of JAX Tracer ...

    Here because the flag ``normalize`` is traced, it cannot be used in Python
    control flow. In this situation, the best solution is probably to mark this
    value as static::

      >>> from functools import partial
      >>> @partial(jit, static_argnames=['normalize'])
      ... def func(x, normalize=True):
      ...   if normalize:
      ...     return x / x.sum()
      ...   return x

      >>> func(jnp.arange(5), True)
      Array([0. , 0.1, 0.2, 0.3, 0.4], dtype=float32)

    For more on ``static_argnums``, see the documentation of :func:`jax.jit`.

  Using non-JAX aware functions
    Another common cause of this error is using non-JAX aware functions within JAX
    code. For example:

      >>> @jit
      ... def func(x):
      ...   return min(x, 0)

      >>> func(2)  # doctest: +IGNORE_EXCEPTION_DETAIL
      Traceback (most recent call last):
          ...
      TracerBoolConversionError: Attempted boolean conversion of JAX Tracer ...

    In this case, the error occurs because Python's built-in ``min`` function is not
    compatible with JAX transforms. This can be fixed by replacing it with
    ``jnp.minumum``:

      >>> @jit
      ... def func(x):
      ...   return jnp.minimum(x, 0)

      >>> print(func(2))
      0

  To understand more subtleties having to do with tracers vs. regular values,
  and concrete vs. abstract values, you may want to read
  :ref:`faq-different-kinds-of-jax-values`.
  """
  def __init__(self, tracer: core.Tracer):
    JAXTypeError.__init__(self,
        f"Attempted boolean conversion of {tracer._error_repr()}."
        f"{tracer._origin_msg()}")
