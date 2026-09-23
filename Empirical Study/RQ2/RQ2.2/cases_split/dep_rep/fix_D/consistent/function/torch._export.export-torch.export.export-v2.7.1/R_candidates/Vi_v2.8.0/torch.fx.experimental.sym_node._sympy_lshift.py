def _sympy_lshift(a, b):
    from torch.utils._sympy.functions import LShift

    return LShift(a, b)
