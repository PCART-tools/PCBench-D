    def string_width_height(self, s):
        """
        Return the string width (including kerning) and string height
        as a (*w*, *h*) tuple.
        """
        if not len(s):
            return 0, 0
        totalw = 0
        namelast = None
        miny = 1e9
        maxy = 0
        for c in s:
            if c == '\n':
                continue
            wx, name, bbox = self._metrics[ord(c)]
            l, b, w, h = bbox

            # find the width with kerning
            try:
                kp = self._kern[(namelast, name)]
            except KeyError:
                kp = 0
            totalw += wx + kp

            # find the max y
            thismax = b + h
            if thismax > maxy:
                maxy = thismax

            # find the min y
            thismin = b
            if thismin < miny:
                miny = thismin
            namelast = name

        return totalw, maxy - miny
