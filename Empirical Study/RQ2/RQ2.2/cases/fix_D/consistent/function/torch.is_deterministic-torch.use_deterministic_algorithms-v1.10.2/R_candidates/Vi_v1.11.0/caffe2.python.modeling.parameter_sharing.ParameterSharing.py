@contextlib.contextmanager
def ParameterSharing(shared_scopes):
    """
    Helper function for sharing scopes.
    All the parameters within the shared_scopes, will be remapped with the
    respect of CurrentNamescope()

    I.e. if one calls ParameterSharing with {'scope_b': 'scope_'a'}, from the
    scope 'some_global_scope', it'll effectively mean, that all parameters from
    'some_global_scope/scope_b' will shared with the parameters from
    'some_global_scope/scope_a'
    """
    assert isinstance(shared_scopes, dict)

    shared_scope_overrides = {}
    current_scope = scope.CurrentNameScope()
    for k, v in shared_scopes.items():
        assert not v.startswith(k), (
            "Illegal override for parameter sharing. {} is prefix of {}".
            format(k, v))
        k = current_scope + k
        v = current_scope + v
        # Normalize all the scopes, so scope_a and scope_a/ are equivalent
        k = _normalize_namescope(k)
        v = _normalize_namescope(v)
        shared_scope_overrides[k] = v

    try:
        parameter_sharing_context.add_scope_overrides(shared_scope_overrides)
        yield
    finally:
        parameter_sharing_context.pop()
