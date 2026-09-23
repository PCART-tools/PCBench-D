    def join(self, a, *args):
        """
        Join given arguments into the same set.  Accepts one or more arguments.
        """
        mapping = self._mapping
        try:
            set_a = mapping[a]
        except KeyError:
            set_a = mapping[a] = weakref.WeakSet([a])
            self._ordering[a] = self._next_order
            self._next_order += 1
        for arg in args:
            try:
                set_b = mapping[arg]
            except KeyError:
                set_b = mapping[arg] = weakref.WeakSet([arg])
                self._ordering[arg] = self._next_order
                self._next_order += 1
            if set_b is not set_a:
                if len(set_b) > len(set_a):
                    set_a, set_b = set_b, set_a
                set_a.update(set_b)
                for elem in set_b:
                    mapping[elem] = set_a
