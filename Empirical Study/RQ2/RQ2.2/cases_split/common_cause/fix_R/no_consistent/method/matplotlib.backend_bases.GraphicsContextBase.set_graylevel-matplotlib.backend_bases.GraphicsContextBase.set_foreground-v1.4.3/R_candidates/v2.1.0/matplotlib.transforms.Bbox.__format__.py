    def __format__(self, fmt):
        return (
            'Bbox(x0={0.x0:{1}}, y0={0.y0:{1}}, x1={0.x1:{1}}, y1={0.y1:{1}})'.
            format(self, fmt))
