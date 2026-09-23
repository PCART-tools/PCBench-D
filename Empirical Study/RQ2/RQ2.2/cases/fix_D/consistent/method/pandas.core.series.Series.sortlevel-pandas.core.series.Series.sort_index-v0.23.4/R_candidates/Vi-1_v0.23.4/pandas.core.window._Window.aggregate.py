    def aggregate(self, arg, *args, **kwargs):
        result, how = self._aggregate(arg, *args, **kwargs)
        if result is None:
            return self.apply(arg, raw=False, args=args, kwargs=kwargs)
        return result
