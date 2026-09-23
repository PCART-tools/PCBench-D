def sym_ite(b, t, f):
    """SymInt-aware utility for ternary operator (``t if b else f``.)"""
    if overrides.has_torch_function((b, t, f)):
        return overrides.handle_torch_function(sym_ite, (b, t, f), b, t, f)
    assert isinstance(b, (SymBool, builtins.bool)) and type(t) == type(f)
    if isinstance(b, SymBool):
        return b.__sym_ite__(t, f)
    return t if b else f
