def _sympy_max(a, b):
    from torch.utils._sympy.functions import Max

    return Max(a, b)
