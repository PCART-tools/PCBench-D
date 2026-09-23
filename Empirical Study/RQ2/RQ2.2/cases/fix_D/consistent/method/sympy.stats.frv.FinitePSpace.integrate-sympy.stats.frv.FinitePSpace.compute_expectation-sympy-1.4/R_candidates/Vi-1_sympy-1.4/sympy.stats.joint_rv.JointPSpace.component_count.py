    @property
    def component_count(self):
        _set = self.distribution.set
        return len(_set.args) if isinstance(_set, ProductSet) else 1
