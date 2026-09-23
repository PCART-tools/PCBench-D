@lu.transformation
def _add_args_(extra_args, *args, **kwargs):
  extra_args = tuple(arg.val for arg in extra_args)
  all_args = (extra_args + args)
  yield (yield all_args, kwargs)
