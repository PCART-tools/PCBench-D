def register_refinement_rule(call_target):
    def register(fn):
        if call_target in _REFINEMENT_RULES:
            raise RuntimeError(f'Refinement rule already registered for {call_target}!')
        _REFINEMENT_RULES[call_target] = fn
        return fn
    return register
