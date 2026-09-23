@export
class TracerIntegerConversionError(JAXTypeError):
  """
  This error can occur when a JAX Tracer object is used in a context where a
  Python integer is expected (see :ref:`faq-different-kinds-of-jax-values` for
  more on what a Tracer is). It typically occurs in a few situations.

  Passing a tracer in place of an integer
    This error can occur if you attempt to pass a traced value to a function
    that requires a static integer argument; for example::

      >>> from jax import jit
      >>> import numpy as np

      >>> @jit
      ... def func(x, axis):
      ...   return np.split(x, 2, axis)

      >>> func(np.arange(4), 0)  # doctest: +IGNORE_EXCEPTION_DETAIL
      Traceback (most recent call last):
          ...
      TracerIntegerConversionError: The __index__() method was called on
      traced array with shape int32[0]

    When this happens, the solution is often to mark the problematic argument as
    static::

      >>> from functools import partial
      >>> @partial(jit, static_argnums=1)
      ... def func(x, axis):
      ...   return np.split(x, 2, axis)

      >>> func(np.arange(10), 0)
      [Array([0, 1, 2, 3, 4], dtype=int32),
       Array([5, 6, 7, 8, 9], dtype=int32)]

    An alternative is to apply the transformation to a closure that encapsulates
    the arguments to be protected, either manually as below or by using
    :func:`functools.partial`::

      >>> jit(lambda arr: np.split(arr, 2, 0))(np.arange(4))
      [Array([0, 1], dtype=int32), Array([2, 3], dtype=int32)]

    **Note a new closure is created at every invocation, which defeats the
    compilation caching mechanism, which is why static_argnums is preferred.**

  Indexing a list with a Tracer
    This error can occur if you attempt to index a Python list with a traced
    quantity.
    For example::

      >>> import jax.numpy as jnp
      >>> from jax import jit

      >>> L = [1, 2, 3]

      >>> @jit
      ... def func(i):
      ...   return L[i]

      >>> func(0)  # doctest: +IGNORE_EXCEPTION_DETAIL
      Traceback (most recent call last):
          ...
      TracerIntegerConversionError: The __index__() method was called on
      traced array with shape int32[0]

    Depending on the context, you can generally fix this either by converting
    the list to a JAX array::

      >>> @jit
      ... def func(i):
      ...   return jnp.array(L)[i]

      >>> func(0)
      Array(1, dtype=int32)

    or by declaring the index as a static argument::

      >>> from functools import partial
      >>> @partial(jit, static_argnums=0)
      ... def func(i):
      ...   return L[i]

      >>> func(0)
      Array(1, dtype=int32, weak_type=True)

  To understand more subtleties having to do with tracers vs. regular values,
  and concrete vs. abstract values, you may want to read
  :ref:`faq-different-kinds-of-jax-values`.
  """
  def __init__(self, tracer: core.Tracer):
    super().__init__(
        f"The __index__() method was called on {tracer._error_repr()}"
        f"{tracer._origin_msg()}")
