  def process_custom_jvp_call(self, primitive, fun, jvp, tracers, **_):
    del primitive, jvp, _  # Unused.
    with new_sublevel():
      return fun.call_wrapped(*tracers)
