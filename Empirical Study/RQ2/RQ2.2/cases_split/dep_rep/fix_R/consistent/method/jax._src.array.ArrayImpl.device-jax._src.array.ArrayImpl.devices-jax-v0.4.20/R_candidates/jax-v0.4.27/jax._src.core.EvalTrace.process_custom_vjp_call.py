  def process_custom_vjp_call(self, primitive, fun, fwd, bwd, tracers, **_):  # pytype: disable=signature-mismatch
    del primitive, fwd, bwd, _  # Unused.
    with new_sublevel():
      return fun.call_wrapped(*tracers)
