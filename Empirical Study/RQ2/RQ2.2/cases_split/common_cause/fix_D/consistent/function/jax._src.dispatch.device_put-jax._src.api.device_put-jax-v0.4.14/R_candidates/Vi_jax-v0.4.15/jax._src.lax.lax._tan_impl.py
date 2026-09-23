@_upcast_fp16_for_computation
def _tan_impl(x):
  return div(sin(x), cos(x))
