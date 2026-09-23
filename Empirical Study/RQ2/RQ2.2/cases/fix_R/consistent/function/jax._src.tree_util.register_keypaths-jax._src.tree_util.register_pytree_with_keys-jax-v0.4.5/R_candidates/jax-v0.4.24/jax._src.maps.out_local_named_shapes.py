@lu.transformation_with_aux
def out_local_named_shapes(local_axes, *args, **kwargs):
  ans = yield args, kwargs
  ans_axes = [frozenset(a.aval.named_shape) & local_axes for a in ans]
  yield ans, ans_axes
