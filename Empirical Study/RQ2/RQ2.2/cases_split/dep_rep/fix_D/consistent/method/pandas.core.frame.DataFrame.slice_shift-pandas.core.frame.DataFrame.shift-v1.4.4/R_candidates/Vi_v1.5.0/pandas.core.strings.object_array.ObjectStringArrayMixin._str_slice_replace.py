    def _str_slice_replace(self, start=None, stop=None, repl=None):
        if repl is None:
            repl = ""

        def f(x):
            if x[start:stop] == "":
                local_stop = start
            else:
                local_stop = stop
            y = ""
            if start is not None:
                y += x[:start]
            y += repl
            if stop is not None:
                y += x[local_stop:]
            return y

        return self._str_map(f)
