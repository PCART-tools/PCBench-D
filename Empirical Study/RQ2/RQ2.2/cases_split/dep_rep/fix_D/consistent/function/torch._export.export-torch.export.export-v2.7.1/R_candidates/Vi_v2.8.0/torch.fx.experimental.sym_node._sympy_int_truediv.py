def _sympy_int_truediv(a, b):
    from torch.utils._sympy.functions import IntTrueDiv

    return IntTrueDiv(a, b)
