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
    _, true_operand, true_fun, false_operand, false_fun = ba.args
    if callable(true_operand) and callable(true_fun):
      # treat this as modern cond (with two operands)
      return _cond(*args, **kwargs)
    if callable(true_fun) and callable(false_fun):
      return _cond_with_per_branch_args(*ba.args)

  return _cond(*args, **kwargs)
