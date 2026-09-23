    def __call__(self, x, pos=None):
        if pos is None:
            return ""
        r_mapping = {v: StrCategoryFormatter._text(k)
                     for k, v in self._units.items()}
        return r_mapping.get(int(np.round(x)), '')
