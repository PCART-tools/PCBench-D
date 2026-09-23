    def __init__(self, name):
        from pandas.core.computation.check import (_NUMEXPR_INSTALLED,
                                                   _NUMEXPR_VERSION)
        if name not in _mathops or (
                _NUMEXPR_INSTALLED and
                _NUMEXPR_VERSION < LooseVersion('2.6.9') and
                name in ('floor', 'ceil')
        ):
            raise ValueError(
                "\"{0}\" is not a supported function".format(name))

        self.name = name
        self.func = getattr(np, name)
