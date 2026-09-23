@lu.transformation
def _argnums_partial(dyn_argnums, fixed_args, *dyn_args, **kwargs):
  sentinel = object()
  args = [sentinel] * (len(fixed_args) + len(dyn_args))
  for i, arg in zip(dyn_argnums, dyn_args):
    args[i] = arg
  fixed_args_ = iter(fixed_args)
  args = [next(fixed_args_).val if x is sentinel else x for x in args]
  assert next(fixed_args_, sentinel) is sentinel
  ans = yield args, kwargs
  yield ans
