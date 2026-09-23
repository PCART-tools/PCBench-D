def assert_discharge_rule(error, enabled_errors, pred, code, payload, *, msgs):
  if ErrorCategory.USER_CHECK not in enabled_errors:
    return [], error

  out_err = error.err | jnp.logical_not(pred)
  out_code = lax.select(error.err, error.code, code)
  return [], Error(out_err, out_code, {**error.msgs, **msgs}, payload)
