    def _str_extract(self, pat: str, flags: int = 0, expand: bool = True):
        regex = re.compile(pat, flags=flags)
        na_value = self._str_na_value

        if not expand:

            def g(x):
                m = regex.search(x)
                return m.groups()[0] if m else na_value

            return self._str_map(g, convert=False)

        empty_row = [na_value] * regex.groups

        def f(x):
            if not isinstance(x, str):
                return empty_row
            m = regex.search(x)
            if m:
                return [na_value if item is None else item for item in m.groups()]
            else:
                return empty_row

        return [f(val) for val in np.asarray(self)]
