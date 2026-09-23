    def aggregate(self, func, *args, **kwargs):
        result, how = self._aggregate(func, *args, **kwargs)
        if result is None:
            return self.apply(func, raw=False, args=args, kwargs=kwargs)
        return result
