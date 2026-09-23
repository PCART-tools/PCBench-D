@lu.transformation
def _argnames_partial(fixed_kwargs: WrapKwArgs, *args, **dyn_kwargs):
  kwargs = dict({k: v.val for k, v in fixed_kwargs.val.items()}, **dyn_kwargs)
  ans = yield args, kwargs
  yield ans
