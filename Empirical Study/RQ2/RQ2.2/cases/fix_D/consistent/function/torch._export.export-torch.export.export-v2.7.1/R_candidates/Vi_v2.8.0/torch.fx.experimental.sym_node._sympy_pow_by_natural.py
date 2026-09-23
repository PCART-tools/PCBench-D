def _sympy_pow_by_natural(a, b):
    from torch.utils._sympy.functions import PowByNatural

    return PowByNatural(a, b)
