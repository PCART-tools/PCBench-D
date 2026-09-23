class TracerArrayConversionError(JAXTypeError):
  """
  This error occurs when a program attempts to convert a JAX Tracer object into
  a standard NumPy array. It typically occurs in one of a few situations.

  Using `numpy` rather than `jax.numpy` functions
    This error can occur when a JAX Tracer object is passed to a raw numpy
    function, or a method on a numpy.ndarray object. For example::

      >>> from functools import partial
      >>> from jax import jit
      >>> import numpy as np
      >>> import jax.numpy as jnp

      >>> @jit
      ... def func(x):
      ...   return np.sin(x)

      >>> func(jnp.arange(4))  # doctest: +IGNORE_EXCEPTION_DETAIL
      Traceback (most recent call last):
          ...
      TracerArrayConversionError: The numpy.ndarray conversion method
      __array__() was called on the JAX Tracer object

    In this case, check that you are using `jax.numpy` methods rather than
    `numpy` methods::

      >>> @jit
      ... def func(x):
      ...   return jnp.sin(x)

      >>> func(jnp.arange(4))
      DeviceArray([0.        , 0.84147096, 0.9092974 , 0.14112   ], dtype=float32)

  Indexing a numpy array with a tracer
    If this error arises on a line that involves array indexing, it may be that
    the array being indexed `x` is a raw numpy.ndarray while the indices `idx`
    are traced. For example::

      >>> x = np.arange(10)

      >>> @jit
      ... def func(i):
      ...   return x[i]

      >>> func(0)  # doctest: +IGNORE_EXCEPTION_DETAIL
      Traceback (most recent call last):
          ...
      TracerArrayConversionError: The numpy.ndarray conversion method
      __array__() was called on the JAX Tracer object

    Depending on the context, you may fix this by converting the numpy array
    into a JAX array::

      >>> @jit
      ... def func(i):
      ...   return jnp.asarray(x)[i]

      >>> func(0)
      DeviceArray(0, dtype=int32)

    or by declaring the index as a static argument::

      >>> @partial(jit, static_argnums=(0,))
      ... def func(i):
      ...   return x[i]

      >>> func(0)
      DeviceArray(0, dtype=int32)

  To understand more subtleties having to do with tracers vs. regular values,
  and concrete vs. abstract values, you may want to read
  :ref:`faq-different-kinds-of-jax-values`.
  """
  def __init__(self, tracer: "core.Tracer"):
    super().__init__(
        "The numpy.ndarray conversion method __array__() was called on "
        f"the JAX Tracer object {tracer}{tracer._origin_msg()}")
