def _sympy_round(number, ndigits=None):
    from torch.utils._sympy.functions import RoundDecimal, RoundToInt

    if ndigits is None:
        return RoundToInt(number)
    else:
        return RoundDecimal(number, ndigits)
