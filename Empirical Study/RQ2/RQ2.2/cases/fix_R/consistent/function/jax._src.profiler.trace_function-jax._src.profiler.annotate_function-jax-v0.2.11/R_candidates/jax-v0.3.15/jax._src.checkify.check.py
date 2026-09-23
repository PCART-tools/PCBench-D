def check(pred: Bool, msg: str) -> None:
  """Check a predicate, add an error with msg if predicate is False.

  This is an effectful operation, and can't be staged (jitted/scanned/...).
  Before staging a function with checks, ``checkify`` it!

  Args:
    pred: if False, an error is added.
    msg: error message if error is added.

  For example:

    >>> import jax
    >>> import jax.numpy as jnp
    >>> from jax.experimental import checkify
    >>> def f(x):
    ...   checkify.check(x!=0, "cannot be zero!")
    ...   return 1/x
    >>> checked_f = checkify.checkify(f)
    >>> err, out = jax.jit(checked_f)(0)
    >>> err.throw()  # doctest: +IGNORE_EXCEPTION_DETAIL
    Traceback (most recent call last):
      ...
    ValueError: cannot be zero! (check failed at ...)

  """
  if not is_scalar_pred(pred):
    raise TypeError(f'check takes a scalar pred as argument, got {pred}')
  code = next_code()
  msg += f' (check failed at {summary()})'
  return check_error(Error(jnp.logical_not(pred), code, {code: msg}))
