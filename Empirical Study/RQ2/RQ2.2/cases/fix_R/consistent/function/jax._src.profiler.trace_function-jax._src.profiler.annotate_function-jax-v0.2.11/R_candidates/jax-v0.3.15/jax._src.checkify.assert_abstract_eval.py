@assert_p.def_effectful_abstract_eval
def assert_abstract_eval(pred, code, payload, *, msgs):
  return [], {CheckEffect}
