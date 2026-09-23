    def aggregate(self, func, *args, **kwargs):
        result = ResamplerWindowApply(self, func, args=args, kwargs=kwargs).agg()
        if result is None:
            return self.apply(func, raw=False, args=args, kwargs=kwargs)
        return result
