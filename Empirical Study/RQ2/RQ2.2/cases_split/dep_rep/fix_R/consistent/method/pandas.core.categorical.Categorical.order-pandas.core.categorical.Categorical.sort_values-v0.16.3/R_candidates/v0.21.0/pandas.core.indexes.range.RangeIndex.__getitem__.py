    def __getitem__(self, key):
        """
        Conserve RangeIndex type for scalar and slice keys.
        """
        super_getitem = super(RangeIndex, self).__getitem__

        if is_scalar(key):
            n = int(key)
            if n != key:
                return super_getitem(key)
            if n < 0:
                n = len(self) + key
            if n < 0 or n > len(self) - 1:
                raise IndexError("index {key} is out of bounds for axis 0 "
                                 "with size {size}".format(key=key,
                                                           size=len(self)))
            return self._start + n * self._step

        if isinstance(key, slice):

            # This is basically PySlice_GetIndicesEx, but delegation to our
            # super routines if we don't have integers

            l = len(self)

            # complete missing slice information
            step = 1 if key.step is None else key.step
            if key.start is None:
                start = l - 1 if step < 0 else 0
            else:
                start = key.start

                if start < 0:
                    start += l
                if start < 0:
                    start = -1 if step < 0 else 0
                if start >= l:
                    start = l - 1 if step < 0 else l

            if key.stop is None:
                stop = -1 if step < 0 else l
            else:
                stop = key.stop

                if stop < 0:
                    stop += l
                if stop < 0:
                    stop = -1
                if stop > l:
                    stop = l

            # delegate non-integer slices
            if (start != int(start) or
                    stop != int(stop) or
                    step != int(step)):
                return super_getitem(key)

            # convert indexes to values
            start = self._start + self._step * start
            stop = self._start + self._step * stop
            step = self._step * step

            return RangeIndex(start, stop, step, self.name, fastpath=True)

        # fall back to Int64Index
        return super_getitem(key)
