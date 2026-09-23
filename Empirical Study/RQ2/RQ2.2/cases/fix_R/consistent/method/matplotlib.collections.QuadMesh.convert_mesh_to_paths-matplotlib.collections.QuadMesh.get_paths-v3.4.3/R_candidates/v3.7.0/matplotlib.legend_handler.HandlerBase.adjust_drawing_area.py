    def adjust_drawing_area(self, legend, orig_handle,
                            xdescent, ydescent, width, height, fontsize,
                            ):
        xdescent = xdescent - self._xpad * fontsize
        ydescent = ydescent - self._ypad * fontsize
        width = width - self._xpad * fontsize
        height = height - self._ypad * fontsize
        return xdescent, ydescent, width, height
