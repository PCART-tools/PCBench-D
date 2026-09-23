    @property
    def corners(self):
        """
        Corners of rectangle in data coordinates from lower left,
        moving clockwise.
        """
        x0, y0, width, height = self._rect_bbox
        xc = x0, x0 + width, x0 + width, x0
        yc = y0, y0, y0 + height, y0 + height
        transform = self._get_rotation_transform()
        coords = transform.transform(np.array([xc, yc]).T).T
        return coords[0], coords[1]
