def _sympy_mod(a, b):
    from torch.utils._sympy.functions import Mod, PythonMod

    if a.is_nonnegative and b.is_nonnegative:
        return Mod(a, b)
    else:
        return PythonMod(a, b)
