    def _is_scalar_access(self, key):
        # this is a shortcut accessor to both .loc and .iloc
        # that provide the equivalent access of .at and .iat
        # a) avoid getting things via sections and (to minimize dtype changes)
        # b) provide a performant path
        if not hasattr(key, '__len__'):
            return False

        if len(key) != self.ndim:
            return False

        for i, k in enumerate(key):
            if not is_integer(k):
                return False

            ax = self.obj.axes[i]
            if not ax.is_unique:
                return False

        return True
