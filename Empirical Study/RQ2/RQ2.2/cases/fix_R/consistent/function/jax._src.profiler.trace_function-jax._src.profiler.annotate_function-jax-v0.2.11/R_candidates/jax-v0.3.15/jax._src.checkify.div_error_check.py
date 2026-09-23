def div_error_check(error, enabled_errors, x, y):
  """Checks for division by zero and NaN."""
  if ErrorCategory.DIV in enabled_errors:
    all_nonzero = jnp.logical_not(jnp.any(jnp.equal(y, 0)))
    msg = f'divided by zero at {summary()}'
    error = assert_func(error, all_nonzero, msg, None)
  return nan_error_check(lax.div_p, error, enabled_errors, x, y)
