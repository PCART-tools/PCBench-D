    def _update_patch_transform(self):
        """
        Notes
        -----
        This cannot be called until after this has been added to an Axes,
        otherwise unit conversion will fail. This makes it very important to
        call the accessor method and not directly access the transformation
        member variable.
        """
        x0, y0, x1, y1 = self._convert_units()
        bbox = transforms.Bbox.from_extents(x0, y0, x1, y1)
        rot_trans = transforms.Affine2D()
        rot_trans.rotate_deg_around(x0, y0, self.angle)
        self._rect_transform = transforms.BboxTransformTo(bbox)
        self._rect_transform += rot_trans
