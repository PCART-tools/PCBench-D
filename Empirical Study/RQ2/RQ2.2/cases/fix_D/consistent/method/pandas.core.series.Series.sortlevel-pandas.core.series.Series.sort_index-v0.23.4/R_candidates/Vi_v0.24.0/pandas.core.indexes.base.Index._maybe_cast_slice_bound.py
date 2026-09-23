    @Appender(_index_shared_docs['_maybe_cast_slice_bound'])
    def _maybe_cast_slice_bound(self, label, side, kind):
        assert kind in ['ix', 'loc', 'getitem', None]

        # We are a plain index here (sub-class override this method if they
        # wish to have special treatment for floats/ints, e.g. Float64Index and
        # datetimelike Indexes
        # reject them
        if is_float(label):
            if not (kind in ['ix'] and (self.holds_integer() or
                                        self.is_floating())):
                self._invalid_indexer('slice', label)

        # we are trying to find integer bounds on a non-integer based index
        # this is rejected (generally .loc gets you here)
        elif is_integer(label):
            self._invalid_indexer('slice', label)

        return label
