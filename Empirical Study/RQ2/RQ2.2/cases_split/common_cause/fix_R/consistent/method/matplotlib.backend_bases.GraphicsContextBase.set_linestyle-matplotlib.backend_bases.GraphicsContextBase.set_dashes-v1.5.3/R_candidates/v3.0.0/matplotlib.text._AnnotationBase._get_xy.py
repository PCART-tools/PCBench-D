    def _get_xy(self, renderer, x, y, s):
        if isinstance(s, tuple):
            s1, s2 = s
        else:
            s1, s2 = s, s

        if s1 == 'data':
            x = float(self.convert_xunits(x))
        if s2 == 'data':
            y = float(self.convert_yunits(y))

        tr = self._get_xy_transform(renderer, s)
        x1, y1 = tr.transform_point((x, y))
        return x1, y1
