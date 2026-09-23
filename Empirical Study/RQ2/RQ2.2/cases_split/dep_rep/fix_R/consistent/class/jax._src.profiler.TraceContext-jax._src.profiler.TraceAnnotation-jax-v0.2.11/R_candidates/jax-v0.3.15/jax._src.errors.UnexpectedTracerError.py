class UnexpectedTracerError(JAXTypeError):
  """
  This error occurs when you use a JAX value that has leaked out of a function.
  What does it mean to leak a value? If you use a JAX transformation on a
  function ``f`` that stores, in some scope outside of ``f``, a reference to
  an intermediate value, that value is considered to have been leaked.
  Leaking values is a side effect. (Read more about avoiding side effects in
  `Pure Functions <https://jax.readthedocs.io/en/latest/notebooks/Common_Gotchas_in_JAX.html#pure-functions>`_)

  JAX detects leaks when you then use the leaked value in another
  operation later on, at which point it raises an ``UnexpectedTracerError``.
  To fix this, avoid side effects: if a function computes a value needed
  in an outer scope, return that value from the transformed function explictly.

  Specifically, a ``Tracer`` is JAX's internal representation of a function's
  intermediate values during transformations, e.g. within ``jit``, ``pmap``,
  ``vmap``, etc. Encountering a ``Tracer`` outside of a transformation implies a
  leak.

  Life-cycle of a leaked value
    Consider the following example of a transformed function which leaks a value
    to an outer scope::

      >>> from jax import jit
      >>> import jax.numpy as jnp

      >>> outs = []
      >>> @jit                   # 1
      ... def side_effecting(x):
      ...   y = x + 1            # 3
      ...   outs.append(y)       # 4

      >>> x = 1
      >>> side_effecting(x)      # 2
      >>> outs[0] + 1            # 5  # doctest: +IGNORE_EXCEPTION_DETAIL
      Traceback (most recent call last):
          ...
      UnexpectedTracerError: Encountered an unexpected tracer.

    In this example we leak a Traced value from an inner transformed scope to an
    outer scope. We get an ``UnexpectedTracerError`` when the leaked value is
    used, not when the value is leaked.

    This example also demonstrates the life-cycle of a leaked value:

      1. A function is transformed (in this case, by ``jit``)
      2. The transformed function is called (initiating an abstract trace of the
         function and turning ``x`` into a ``Tracer``)
      3. The intermediate value ``y``, which will later be leaked, is created
         (an intermediate value of a traced function is also a ``Tracer``)
      4. The value is leaked (appended to a list in an outer scope, escaping
         the function through a side-channel)
      5. The leaked value is used, and an UnexpectedTracerError is raised.

    The UnexpectedTracerError message tries to point to these locations in your
    code by including information about each stage. Respectively:

      1. The name of the transformed function (``side_effecting``) and which
         transform kicked of the trace (``jit``).
      2. A reconstructed stack trace of where the leaked Tracer was created,
         which includes where the transformed function was called.
         (``When the Tracer was created, the final 5 stack frames were...``).
      3. From the reconstructed stack trace, the line of code that created
         the leaked Tracer.
      4. The leak location is not included in the error message because it is
         difficult to pin down! JAX can only tell you what the leaked value
         looks like (what shape is has and where it was created) and what
         boundary it was leaked over (the name of the transformation and the
         name of the transformed function).
      5. The current error's stack trace points to where the value is used.

    The error can be fixed by the returning the value out of the
    transformed function::

      >>> from jax import jit
      >>> import jax.numpy as jnp

      >>> outs = []
      >>> @jit
      ... def not_side_effecting(x):
      ...   y = x+1
      ...   return y

      >>> x = 1
      >>> y = not_side_effecting(x)
      >>> outs.append(y)
      >>> outs[0] + 1  # all good! no longer a leaked value.
      DeviceArray(3, dtype=int32, weak_type=True)

  Leak checker
    As discussed in point 2 and 3 above, JAX shows a reconstructed stack trace
    which points to where the leaked value was created.  This is because
    JAX only raises an error when the leaked value is used, not when the
    value is leaked. This is not the most useful place to raise this error,
    because you need to know the location where the Tracer was leaked to fix the
    error.

    To make this location easier to track down, you can use the leak checker.
    When the leak checker is enabled, an error is raised as soon as a ``Tracer``
    is leaked. (To be more exact, it will raise an error when the transformed
    function from which the ``Tracer`` is leaked returns)

    To enable the leak checker you can use the ``JAX_CHECK_TRACER_LEAKS``
    environment variable or the ``with jax.checking_leaks()`` context manager.

    .. note::
      Note that this tool is experimental and may report false positives. It
      works by disabling some JAX caches, so it will have a negative effect on
      performance and should only be used when debugging.

    Example usage::

      >>> from jax import jit
      >>> import jax.numpy as jnp

      >>> outs = []
      >>> @jit
      ... def side_effecting(x):
      ...   y = x+1
      ...   outs.append(y)

      >>> x = 1
      >>> with jax.checking_leaks():
      ...   y = side_effecting(x)  # doctest: +IGNORE_EXCEPTION_DETAIL
      Traceback (most recent call last):
          ...
      Exception: Leaked Trace

  """

  def __init__(self, msg: str):
    super().__init__(msg)
