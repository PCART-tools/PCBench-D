@assert_p.def_impl
def assert_impl(pred, code, payload, *, msgs):
  Error(~pred, code, msgs, payload).throw()
  return []
