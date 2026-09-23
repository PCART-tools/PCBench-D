def register_algebraic_expressions_inference_rule(call_target):
    def register(fn):
        if call_target in _RULES:
            raise RuntimeError(f'Rule already registered for {call_target}!')
        _RULES[call_target] = fn
        return fn
    return register
