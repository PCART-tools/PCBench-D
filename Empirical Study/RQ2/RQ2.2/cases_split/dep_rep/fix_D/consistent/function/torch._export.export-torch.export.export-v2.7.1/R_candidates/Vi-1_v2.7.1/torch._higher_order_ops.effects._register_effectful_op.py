def _register_effectful_op(op: OpType, effect: _EffectType):
    assert isinstance(
        op, (torch._ops.OpOverload, torch._ops.HigherOrderOperator)
    ) and not has_aliasing(op)
    if op in SIDE_EFFECTS and SIDE_EFFECTS[op] != effect:
        raise RuntimeError(
            f"Already registered effect type {SIDE_EFFECTS[op]} to op {op}, "
            f"trying to register a different effect type {effect}."
        )
    SIDE_EFFECTS[op] = effect
