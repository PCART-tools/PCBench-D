    def _update_patch_transform(self):
        """NOTE: This cannot be called until after this has been added
                 to an Axes, otherwise unit conversion will fail. This
                 maxes it very important to call the accessor method and
                 not directly access the transformation member variable.
        """
        x = self.convert_xunits(self._x)
        y = self.convert_yunits(self._y)
        width = self.convert_xunits(self._width)
        height = self.convert_yunits(self._height)
        bbox = transforms.Bbox.from_bounds(x, y, width, height)
        rot_trans = transforms.Affine2D()
        rot_trans.rotate_deg_around(x, y, self.angle)
        self._rect_transform = transforms.BboxTransformTo(bbox)
        self._rect_transform += rot_trans
