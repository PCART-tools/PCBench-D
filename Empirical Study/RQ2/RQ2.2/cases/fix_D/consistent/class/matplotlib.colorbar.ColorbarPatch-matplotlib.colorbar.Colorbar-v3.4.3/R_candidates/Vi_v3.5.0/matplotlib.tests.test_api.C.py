    class C:
        def __init__(self): self._attr = 1
        def _meth(self, arg): return arg
        attr = _api.deprecate_privatize_attribute("0.0")
        meth = _api.deprecate_privatize_attribute("0.0")
