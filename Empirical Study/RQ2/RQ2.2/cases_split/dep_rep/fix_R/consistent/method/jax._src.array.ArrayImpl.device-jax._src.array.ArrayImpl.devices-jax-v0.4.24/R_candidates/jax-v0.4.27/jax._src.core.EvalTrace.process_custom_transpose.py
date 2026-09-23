  def process_custom_transpose(self, primitive, call, tracers, **_):
    del primitive, _
    with new_sublevel():
      return call.call_wrapped(*tracers)
