    def join(self, a, *args):
        """
        Join given arguments into the same set.  Accepts one or more arguments.
        """
        mapping = self._mapping
        set_a = mapping.setdefault(weakref.ref(a), [weakref.ref(a)])

        for arg in args:
            set_b = mapping.get(weakref.ref(arg), [weakref.ref(arg)])
            if set_b is not set_a:
                if len(set_b) > len(set_a):
                    set_a, set_b = set_b, set_a
                set_a.extend(set_b)
                for elem in set_b:
                    mapping[elem] = set_a

        self.clean()
