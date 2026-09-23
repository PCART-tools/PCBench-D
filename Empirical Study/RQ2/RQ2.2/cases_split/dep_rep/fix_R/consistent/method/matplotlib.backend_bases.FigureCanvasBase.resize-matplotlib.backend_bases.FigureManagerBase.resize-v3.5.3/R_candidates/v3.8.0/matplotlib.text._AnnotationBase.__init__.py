    def __init__(self,
                 xy,
                 xycoords='data',
                 annotation_clip=None):

        x, y = xy  # Make copy when xy is an array (and check the shape).
        self.xy = x, y
        self.xycoords = xycoords
        self.set_annotation_clip(annotation_clip)

        self._draggable = None
