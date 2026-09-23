def _sympy_floordiv(a, b):
    from torch.utils._sympy.functions import FloorDiv

    return FloorDiv(a, b)
