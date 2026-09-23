def _sympy_floor(a):
    from torch.utils._sympy.functions import FloorToInt

    return FloorToInt(a)
