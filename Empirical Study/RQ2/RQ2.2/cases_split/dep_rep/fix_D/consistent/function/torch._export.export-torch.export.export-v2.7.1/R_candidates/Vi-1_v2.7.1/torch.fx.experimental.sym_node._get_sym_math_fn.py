def _get_sym_math_fn(name):
    def fn(a):
        import torch.utils._sympy.functions

        return getattr(torch.utils._sympy.functions, f"OpaqueUnaryFn_{name}")(a)

    return fn
