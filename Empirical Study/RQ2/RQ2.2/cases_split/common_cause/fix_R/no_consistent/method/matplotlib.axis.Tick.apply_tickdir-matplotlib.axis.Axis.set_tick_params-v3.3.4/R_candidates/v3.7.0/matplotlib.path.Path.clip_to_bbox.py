    def clip_to_bbox(self, bbox, inside=True):
        """
        Clip the path to the given bounding box.

        The path must be made up of one or more closed polygons.  This
        algorithm will not behave correctly for unclosed paths.

        If *inside* is `True`, clip to the inside of the box, otherwise
        to the outside of the box.
        """
        verts = _path.clip_path_to_rect(self, bbox, inside)
        paths = [Path(poly) for poly in verts]
        return self.make_compound_path(*paths)
