def _sympy_rshift(a, b):
    from torch.utils._sympy.functions import RShift

    return RShift(a, b)
