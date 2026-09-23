def assert_func(error: Error, pred: Bool, msg: str,
                payload: Optional[Payload]) -> Error:
  code = next_code()
  payload = init_payload if payload is None else payload
  out_err = error.err | jnp.logical_not(pred)
  out_code = lax.select(error.err, error.code, code)
  out_payload = lax.select(error.err, error.payload, payload)
  return Error(out_err, out_code, {code: msg, **error.msgs}, out_payload)
