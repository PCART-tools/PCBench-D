    def _aggregate(self, arg, axis=0, *args, **kwargs):
        if axis == 1:
            # NDFrame.aggregate returns a tuple, and we need to transpose
            # only result
            result, how = self.T._aggregate(arg, *args, **kwargs)
            result = result.T if result is not None else result
            return result, how
        return super()._aggregate(arg, *args, **kwargs)
