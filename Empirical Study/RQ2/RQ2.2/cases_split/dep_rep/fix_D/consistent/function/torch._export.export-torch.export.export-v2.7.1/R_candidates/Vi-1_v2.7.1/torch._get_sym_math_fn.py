def _get_sym_math_fn(name):
    def fn(a):
        if overrides.has_torch_function_unary(a):
            return overrides.handle_torch_function(fn, (a,), a)
        if isinstance(a, SymInt):
            a = torch.sym_float(a)
        if hasattr(a, f"__sym_{name}__"):
            return getattr(a, f"__sym_{name}__")()
        return getattr(math, name)(a)

    return fn
