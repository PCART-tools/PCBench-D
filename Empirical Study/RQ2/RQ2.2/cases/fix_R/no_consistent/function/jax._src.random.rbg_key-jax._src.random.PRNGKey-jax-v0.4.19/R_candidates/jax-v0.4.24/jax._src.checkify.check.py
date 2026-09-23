def check(pred: Bool, msg: str, *fmt_args, **fmt_kwargs) -> None:
  """Check a predicate, add an error with msg if predicate is False.

  This is an effectful operation, and can't be staged (jitted/scanned/...).
  Before staging a function with checks, :func:`~checkify` it!

  Args:
    pred: if False, a FailedCheckError error is added.
    msg: error message if error is added. Can be a format string.
    fmt_args, fmt_kwargs: Positional and keyword formatting arguments for
      `msg`, eg.:
      ``check(.., "check failed on values {} and {named_arg}", x, named_arg=y)``
      Note that these arguments can be traced values allowing you to add
      run-time values to the error message.
      Note that tracking these run-time arrays will increase your memory usage,
      even if no error happens.

  For example:

    >>> import jax
    >>> import jax.numpy as jnp
    >>> from jax.experimental import checkify
    >>> def f(x):
    ...   checkify.check(x>0, "{x} needs to be positive!", x=x)
    ...   return 1/x
    >>> checked_f = checkify.checkify(f)
    >>> err, out = jax.jit(checked_f)(-3.)
    >>> err.throw()  # doctest: +IGNORE_EXCEPTION_DETAIL
    Traceback (most recent call last):
      ...
    jax._src.checkify.JaxRuntimeError: -3. needs to be positive!

  """
  _check(pred, msg, False, *fmt_args, **fmt_kwargs)
