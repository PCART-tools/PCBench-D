@export
class TracerArrayConversionError(JAXTypeError):
  """
  This error occurs when a program attempts to convert a JAX Tracer object into
  a standard NumPy array (see :ref:`faq-different-kinds-of-jax-values` for more
  on what a Tracer is). It typically occurs in one of a few situations.

  Using non-JAX functions in JAX transformations
    This error can occur if you attempt to use a non-JAX library like ``numpy``
    or ``scipy`` inside a JAX transformation (:func:`~jax.jit`, :func:`~jax.grad`,
    :func:`jax.vmap`, etc.). For example::

      >>> from jax import jit
      >>> import numpy as np

      >>> @jit
      ... def func(x):
      ...   return np.sin(x)

      >>> func(np.arange(4))  # doctest: +IGNORE_EXCEPTION_DETAIL
      Traceback (most recent call last):
          ...
      TracerArrayConversionError: The numpy.ndarray conversion method
      __array__() was called on traced array with shape int32[4]

    In this case, you can fix the issue by using :func:`jax.numpy.sin` in place of
    :func:`numpy.sin`::

      >>> import jax.numpy as jnp
      >>> @jit
      ... def func(x):
      ...   return jnp.sin(x)

      >>> func(jnp.arange(4))
      Array([0.        , 0.84147096, 0.9092974 , 0.14112   ], dtype=float32)

    See also `External Callbacks`_ for options for calling back to host-side computations
    from transformed JAX code.

  Indexing a numpy array with a tracer
    If this error arises on a line that involves array indexing, it may be that
    the array being indexed ``x`` is a standard numpy.ndarray while the indices
    ``idx`` are traced JAX arrays. For example::

      >>> x = np.arange(10)

      >>> @jit
      ... def func(i):
      ...   return x[i]

      >>> func(0)  # doctest: +IGNORE_EXCEPTION_DETAIL
      Traceback (most recent call last):
          ...
      TracerArrayConversionError: The numpy.ndarray conversion method
      __array__() was called on traced array with shape int32[0]

    Depending on the context, you may fix this by converting the numpy array
    into a JAX array::

      >>> @jit
      ... def func(i):
      ...   return jnp.asarray(x)[i]

      >>> func(0)
      Array(0, dtype=int32)

    or by declaring the index as a static argument::

      >>> from functools import partial
      >>> @partial(jit, static_argnums=(0,))
      ... def func(i):
      ...   return x[i]

      >>> func(0)
      Array(0, dtype=int32)

  To understand more subtleties having to do with tracers vs. regular values,
  and concrete vs. abstract values, you may want to read
  :ref:`faq-different-kinds-of-jax-values`.

  .. _External Callbacks: https://jax.readthedocs.io/en/latest/notebooks/external_callbacks.html
  """
  def __init__(self, tracer: core.Tracer):
    super().__init__(
        "The numpy.ndarray conversion method __array__() was called on "
        f"{tracer._error_repr()}{tracer._origin_msg()}")
