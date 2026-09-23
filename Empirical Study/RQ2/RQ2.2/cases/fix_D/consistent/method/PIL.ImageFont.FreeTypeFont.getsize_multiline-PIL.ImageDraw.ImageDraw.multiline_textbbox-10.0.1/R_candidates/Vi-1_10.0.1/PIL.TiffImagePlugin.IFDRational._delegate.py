    def _delegate(op):
        def delegate(self, *args):
            return getattr(self._val, op)(*args)

        return delegate
