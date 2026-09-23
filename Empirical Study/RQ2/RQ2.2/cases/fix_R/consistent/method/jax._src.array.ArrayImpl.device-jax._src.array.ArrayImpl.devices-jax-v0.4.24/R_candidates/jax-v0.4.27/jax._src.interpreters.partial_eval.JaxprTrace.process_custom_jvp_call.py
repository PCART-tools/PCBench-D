  def process_custom_jvp_call(self, prim, fun, jvp, tracers, *, symbolic_zeros):
    # We assume partial evaluation is only performed to build linear functions,
    # and hence we don't need to keep the custom JVP rule around anymore.
    del jvp, symbolic_zeros
    assert not all(t.is_known() for t in tracers)
    return fun.call_wrapped(*tracers)
