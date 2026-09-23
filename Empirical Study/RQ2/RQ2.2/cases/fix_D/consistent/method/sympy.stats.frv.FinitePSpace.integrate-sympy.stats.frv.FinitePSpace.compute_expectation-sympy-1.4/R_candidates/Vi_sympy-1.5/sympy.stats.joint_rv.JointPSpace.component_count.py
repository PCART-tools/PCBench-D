    @property
    def component_count(self):
        _set = self.distribution.set
        if isinstance(_set, ProductSet):
            return S(len(_set.args))
        elif isinstance(_set, Product):
            return _set.limits[0][-1]
        return S.One
