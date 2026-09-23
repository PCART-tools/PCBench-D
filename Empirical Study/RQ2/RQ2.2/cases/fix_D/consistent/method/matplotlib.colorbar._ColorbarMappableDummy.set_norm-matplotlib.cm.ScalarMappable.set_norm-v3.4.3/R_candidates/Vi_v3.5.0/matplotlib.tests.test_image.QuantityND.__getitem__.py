    def __getitem__(self, item):
        units = getattr(self, "units", None)
        ret = super(QuantityND, self).__getitem__(item)
        if isinstance(ret, QuantityND) or units is not None:
            ret = QuantityND(ret, units)
        return ret
