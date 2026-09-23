def _cond_with_per_branch_args(pred,
                               true_operand, true_fun: Callable,
                               false_operand, false_fun: Callable):
  """Conditionally apply ``true_fun`` or ``false_fun``.

  Has equivalent semantics to this Python implementation::

    def cond(pred, true_operand, true_fun, false_operand, false_fun):
      if pred:
        return true_fun(true_operand)
      else:
        return false_fun(false_operand)

  Pred has to be a scalar type, collection types (list, tuple) are not supported
  """
  if not (callable(true_fun) and callable(false_fun)):
    raise TypeError("lax.cond: true_fun and false_fun arguments should be callable.")
  return _cond(pred,
               lambda op: true_fun(op[0]),
               lambda op: false_fun(op[1]),
               (true_operand, false_operand))
