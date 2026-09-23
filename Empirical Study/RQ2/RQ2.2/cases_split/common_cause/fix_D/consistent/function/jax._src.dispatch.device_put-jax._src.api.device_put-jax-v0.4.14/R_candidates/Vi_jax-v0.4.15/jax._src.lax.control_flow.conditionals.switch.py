@api_boundary
def switch(index, branches: Sequence[Callable], *operands,
           operand=_no_operand_sentinel):
  """Apply exactly one of ``branches`` given by ``index``.

  If ``index`` is out of bounds, it is clamped to within bounds.

  Has the semantics of the following Python::

    def switch(index, branches, *operands):
      index = clamp(0, index, len(branches) - 1)
      return branches[index](*operands)

  Internally this wraps XLA's `Conditional
  <https://www.tensorflow.org/xla/operation_semantics#conditional>`_
  operator. However, when transformed with :func:`~jax.vmap` to operate over a
  batch of predicates, ``cond`` is converted to :func:`~jax.lax.select`.

  Args:
    index: Integer scalar type, indicating which branch function to apply.
    branches: Sequence of functions (A -> B) to be applied based on ``index``.
    operands: Operands (A) input to whichever branch is applied.

  Returns:
    Value (B) of ``branch(*operands)`` for the branch that was selected based
    on ``index``.
  """
  if not all(callable(branch) for branch in branches):
    raise TypeError("lax.switch: branches argument should be a sequence of callables.")
  if operand is not _no_operand_sentinel:
    if operands:
      raise TypeError("if 'operand' keyword is passed then no positional "
                      f"operands can be passed, got {operand=} "
                      f"and positional operands {operands}")
    operands = (operand,)
  del operand

  if len(np.shape(index)) != 0:
    raise TypeError(
        f"Branch index must be scalar, "
        f"got {index} of shape {np.shape(index)}.")

  try:
    index_dtype = dtypes.result_type(index)
  except TypeError as err:
    msg = f"Index type must be an integer, got {index}."
    raise TypeError(msg) from err

  if index_dtype.kind not in 'iu':
    raise TypeError(
        f"Index type must be an integer, got {index} as {index_dtype}")

  branches = tuple(branches)

  if len(branches) == 0:
    raise ValueError("Empty branch sequence")
  elif len(branches) == 1:
    return branches[0](*operands)

  index = lax.convert_element_type(index, np.int32)
  lo = np.array(0, np.int32)
  hi = np.array(len(branches) - 1, np.int32)
  index = lax.clamp(lo, index, hi)

  if (config.jax_disable_jit and
      isinstance(core.get_aval(index), ConcreteArray)):
    return branches[int(index)](*operands)

  ops, ops_tree = tree_flatten(operands)
  ops_avals = tuple(map(_abstractify, ops))

  jaxprs, consts, out_trees = _initial_style_jaxprs_with_common_consts(
      branches, ops_tree, ops_avals, primitive_name='switch')
  for i, (out_tree, jaxpr) in enumerate(zip(out_trees[1:], jaxprs[1:])):
    _check_tree_and_avals(f"branch 0 and {i + 1} outputs",
                          out_trees[0], jaxprs[0].out_avals,
                          out_tree, jaxpr.out_avals)
  joined_effects = core.join_effects(*(jaxpr.effects for jaxpr in jaxprs))
  disallowed_effects = allowed_effects.filter_not_in(joined_effects)
  if disallowed_effects:
    raise NotImplementedError(
        f'Effects not supported in `switch`: {disallowed_effects}')
  if joined_effects:
    # Raise index in case of effects to allow data-dependence-based discharging
    # of those effects (even if they don't have an explicit data dependence).
    index = core.raise_as_much_as_possible(index)

  linear = (False,) * (len(consts) + len(ops))
  out = cond_p.bind(
      index, *consts, *ops, branches=tuple(jaxprs), linear=linear)
  return tree_unflatten(out_trees[0], out)
