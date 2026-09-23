def _sympy_trunc(a):
    from torch.utils._sympy.functions import TruncToInt

    return TruncToInt(a)
