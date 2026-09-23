    def get_str_bbox_and_descent(self, s):
        """
        Return the string bounding box
        """
        if not len(s):
            return 0, 0, 0, 0
        totalw = 0
        namelast = None
        miny = 1e9
        maxy = 0
        left = 0
        if not isinstance(s, six.text_type):
            s = _to_str(s)
        for c in s:
            if c == '\n':
                continue
            name = uni2type1.get(ord(c), 'question')
            try:
                wx, bbox = self._metrics_by_name[name]
            except KeyError:
                name = 'question'
                wx, bbox = self._metrics_by_name[name]
            l, b, w, h = bbox
            if l < left:
                left = l
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

        return left, miny, totalw, maxy - miny, -miny
