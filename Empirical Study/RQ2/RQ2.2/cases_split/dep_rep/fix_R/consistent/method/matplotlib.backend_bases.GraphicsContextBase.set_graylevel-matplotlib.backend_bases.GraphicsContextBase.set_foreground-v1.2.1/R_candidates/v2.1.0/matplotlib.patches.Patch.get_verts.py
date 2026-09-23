    def get_verts(self):
        """
        Return a copy of the vertices used in this patch

        If the patch contains Bezier curves, the curves will be
        interpolated by line segments.  To access the curves as
        curves, use :meth:`get_path`.
        """
        trans = self.get_transform()
        path = self.get_path()
        polygons = path.to_polygons(trans)
        if len(polygons):
            return polygons[0]
        return []
