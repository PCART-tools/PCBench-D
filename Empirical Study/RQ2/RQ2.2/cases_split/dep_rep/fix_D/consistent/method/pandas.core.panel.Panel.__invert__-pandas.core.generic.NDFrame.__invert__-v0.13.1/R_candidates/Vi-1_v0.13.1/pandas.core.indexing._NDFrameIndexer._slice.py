    def _slice(self, obj, axis=0, raise_on_error=False, typ=None):
        return self.obj._slice(obj, axis=axis, raise_on_error=raise_on_error,
                               typ=typ)
