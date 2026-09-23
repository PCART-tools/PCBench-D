@api_boundary
@functools.wraps(_cond)
def cond(*args, **kwargs):
  # detect an attempt to call the former, deprecated cond
  try:
    ba = inspect.signature(_cond_with_per_branch_args).bind(*args, **kwargs)
  except TypeError:
    pass
  else:
    assert not ba.kwargs  # no catch-all **kwargs in _cond_with_per_branch
    _, _, maybe_true_fun, _, maybe_false_fun = ba.args
    if callable(maybe_true_fun) and callable(maybe_false_fun):
      return _cond_with_per_branch_args(*ba.args)

  return _cond(*args, **kwargs)
