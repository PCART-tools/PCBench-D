def _sympy_min(a, b):
    from torch.utils._sympy.functions import Min

    return Min(a, b)
