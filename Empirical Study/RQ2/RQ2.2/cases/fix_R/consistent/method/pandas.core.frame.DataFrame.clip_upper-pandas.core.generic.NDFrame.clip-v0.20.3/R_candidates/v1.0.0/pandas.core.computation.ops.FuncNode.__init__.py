    def __init__(self, name: str):
        from pandas.core.computation.check import _NUMEXPR_INSTALLED, _NUMEXPR_VERSION

        if name not in _mathops or (
            _NUMEXPR_INSTALLED
            and _NUMEXPR_VERSION < LooseVersion("2.6.9")
            and name in ("floor", "ceil")
        ):
            raise ValueError(f'"{name}" is not a supported function')

        self.name = name
        self.func = getattr(np, name)
