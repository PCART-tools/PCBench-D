class EvalTrace(Trace):
  # See comments in https://github.com/google/jax/pull/3370
  def pure(self, x): return x
  lift = sublift = pure

  def process_primitive(self, primitive, tracers, params):
    return primitive.impl(*tracers, **params)

  def process_call(self, primitive, f, tracers, params):
    return primitive.impl(f, *tracers, **params)
  process_map = process_call

  def process_custom_transpose(self, primitive, call, tracers, **_):
    del primitive, _
    with new_sublevel():
      return call.call_wrapped(*tracers)

  def process_custom_jvp_call(self, primitive, fun, jvp, tracers, **_):
    del primitive, jvp, _  # Unused.
    with new_sublevel():
      return fun.call_wrapped(*tracers)

  def process_custom_vjp_call(self, primitive, fun, fwd, bwd, tracers, **_):  # pytype: disable=signature-mismatch
    del primitive, fwd, bwd, _  # Unused.
    with new_sublevel():
      return fun.call_wrapped(*tracers)
