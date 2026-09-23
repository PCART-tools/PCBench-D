def _maybe_get_opdef(
    op: Union[CustomOpDef, _ops.OpOverload, str]
) -> Optional[CustomOpDef]:
    if isinstance(op, CustomOpDef):
        return op
    if isinstance(op, _ops.OpOverload):
        op = op._name
    assert isinstance(op, str)
    if op in OPDEFS:
        return OPDEFS[op]
    return None
