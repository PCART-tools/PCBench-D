def _cond(pred, true_fun: Callable, false_fun: Callable, *operands,
          operand=_no_operand_sentinel, linear=None):
  """Conditionally apply ``true_fun`` or ``false_fun``.

  ``cond()`` has equivalent semantics to this Python implementation::

    def cond(pred, true_fun, false_fun, *operands):
      if pred:
        return true_fun(*operands)
      else:
        return false_fun(*operands)

  ``pred`` must be a scalar type.

  Args:
    pred: Boolean scalar type, indicating which branch function to apply.
    true_fun: Function (A -> B), to be applied if ``pred`` is True.
    false_fun: Function (A -> B), to be applied if ``pred`` is False.
    operands: Operands (A) input to either branch depending on ``pred``. The
      type can be a scalar, array, or any pytree (nested Python tuple/list/dict)
      thereof.

  Returns:
    Value (B) of either ``true_fun(*operands)`` or ``false_fun(*operands)``,
    depending on the value of ``pred``. The type can be a scalar, array, or any
    pytree (nested Python tuple/list/dict) thereof.
  """
  if not (callable(true_fun) and callable(false_fun)):
    raise TypeError("lax.cond: true_fun and false_fun arguments should be callable.")
  if operand is not _no_operand_sentinel:
    if operands:
      raise TypeError("if 'operand' keyword is passed then no positional "
                      f"operands can be passed, got operand={operand} "
                      f"and positional operands {operands}")
    operands = (operand,)
  del operand

  if isinstance(pred, Sequence) or np.ndim(pred) != 0:
    raise TypeError(
        f"Pred must be a scalar, got {pred} of " +
        (f"type {type(pred)}" if isinstance(pred, Sequence)
         else f"shape {np.shape(pred)}."))

  try:
    pred_dtype = dtypes.result_type(pred)
  except TypeError as err:
    msg = ("Pred type must be either boolean or number, got {}.")
    raise TypeError(msg.format(pred)) from err

  if pred_dtype.kind != 'b':
    if pred_dtype.kind in 'iuf':
      pred = pred != 0
    else:
      msg = ("Pred type must be either boolean or number, got {}.")
      raise TypeError(msg.format(pred_dtype))

  if config.jax_disable_jit and isinstance(core.get_aval(pred), ConcreteArray):
    if pred:
      return true_fun(*operands)
    else:
      return false_fun(*operands)

  ops, ops_tree = tree_flatten(operands)
  if linear is None:
    linear_ops = [False] * len(ops)
  else:
    linear_ops, ops_tree2 = tree_flatten(linear)
    if ops_tree != ops_tree2:
      raise TypeError('linear tree and operand tree mismatch')
  ops_avals = tuple(_map(_abstractify, ops))

  jaxprs, consts, out_trees = _initial_style_jaxprs_with_common_consts(
      (true_fun, false_fun), ops_tree, ops_avals, 'cond')
  true_jaxpr, false_jaxpr = jaxprs
  out_tree, false_out_tree = out_trees

  _check_tree_and_avals("true_fun and false_fun output",
                        out_tree, true_jaxpr.out_avals,
                        false_out_tree, false_jaxpr.out_avals)
  joined_effects = core.join_effects(true_jaxpr.effects, false_jaxpr.effects)
  disallowed_effects = joined_effects - allowed_effects
  if disallowed_effects:
    raise NotImplementedError(
        f'Effects not supported in `cond`: {disallowed_effects}')

  index = lax.convert_element_type(pred, np.int32)

  linear = [False] * len(consts) + linear_ops
  out = cond_p.bind(
      index, *consts, *ops,
      branches=(false_jaxpr, true_jaxpr), linear=tuple(linear))
  return tree_unflatten(out_tree, out)
