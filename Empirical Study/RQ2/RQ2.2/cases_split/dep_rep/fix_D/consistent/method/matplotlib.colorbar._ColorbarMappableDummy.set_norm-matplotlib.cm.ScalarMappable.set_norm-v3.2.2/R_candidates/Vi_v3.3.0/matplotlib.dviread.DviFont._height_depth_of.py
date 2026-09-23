    def _height_depth_of(self, char):
        """Height and depth of char in dvi units."""
        result = []
        for metric, name in ((self._tfm.height, "height"),
                             (self._tfm.depth, "depth")):
            value = metric.get(char, None)
            if value is None:
                _log.debug('No %s for char %d in font %s',
                           name, char, self.texname)
                result.append(0)
            else:
                result.append(_mul2012(value, self._scale))
        # cmsy10 glyph 0 ("minus") has a nonzero descent so that TeX aligns
        # equations properly (https://tex.stackexchange.com/questions/526103/),
        # but we actually care about the rasterization depth to align the
        # dvipng-generated images.
        if self.texname == b"cmsy10" and char == 0:
            result[-1] = 0
        return result
