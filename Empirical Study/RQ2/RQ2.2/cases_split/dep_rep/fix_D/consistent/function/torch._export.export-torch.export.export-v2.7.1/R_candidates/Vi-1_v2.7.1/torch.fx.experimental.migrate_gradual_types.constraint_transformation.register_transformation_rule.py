def register_transformation_rule(call_target):
    def register(fn):
        if call_target in _TRANSFORMATION_RULES:
            raise RuntimeError(
                f"Transformation rule already registered for {call_target}!"
            )
        _TRANSFORMATION_RULES[call_target] = fn
        return fn

    return register
