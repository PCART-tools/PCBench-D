def _sympy_ceil(a):
    from torch.utils._sympy.functions import CeilToInt

    return CeilToInt(a)
