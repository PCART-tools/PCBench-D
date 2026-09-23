    def _keys(self, *args):
        if not args:
            try:
                return self._cached_keys
            except AttributeError:
                pass

        if not self.chunks:
            return [(self.name,)]
        ind = len(args)
        if ind + 1 == self.ndim:
            result = [(self.name,) + args + (i,)
                      for i in range(self.numblocks[ind])]
        else:
            result = [self._keys(*(args + (i,)))
                      for i in range(self.numblocks[ind])]
        if not args:
            self._cached_keys = result
        return result
