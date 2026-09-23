    def rotated(self, radians):
        """
        Return a new bounding box that bounds a rotated version of
        this bounding box by the given radians.  The new bounding box
        is still aligned with the axes, of course.
        """
        corners = self.corners()
        corners_rotated = Affine2D().rotate(radians).transform(corners)
        bbox = Bbox.unit()
        bbox.update_from_data_xy(corners_rotated, ignore=True)
        return bbox
