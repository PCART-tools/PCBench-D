def get_effect_key(op, args, kwargs) -> Optional[_EffectType]:
    if op in SIDE_EFFECTS:
        return SIDE_EFFECTS[op]

    for arg in args:
        if isinstance(arg, (torch.ScriptObject, FakeScriptObject)):
            # Add it to the table so that next time we see the same op we don't
            # have to parse through the args again
            SIDE_EFFECTS[op] = _EffectType.ORDERED
            return _EffectType.ORDERED

    return None
