def _sympy_float_pow(a, b):
    from torch.utils._sympy.functions import FloatPow

    return FloatPow(a, b)
