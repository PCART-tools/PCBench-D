    def aggregate(self, arg, *args, **kwargs):
        result, how = self._aggregate(arg, *args, **kwargs)
        if result is None:
            result = self._downsample(arg, *args, **kwargs)

        result = self._apply_loffset(result)
        return result
