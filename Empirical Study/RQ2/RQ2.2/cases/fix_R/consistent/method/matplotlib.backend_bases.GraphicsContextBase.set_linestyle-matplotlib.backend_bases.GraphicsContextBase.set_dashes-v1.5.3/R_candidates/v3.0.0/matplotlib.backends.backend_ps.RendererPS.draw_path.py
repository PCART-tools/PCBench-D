    def draw_path(self, gc, path, transform, rgbFace=None):
        """
        Draws a Path instance using the given affine transform.
        """
        clip = rgbFace is None and gc.get_hatch_path() is None
        simplify = path.should_simplify and clip
        ps = self._convert_path(path, transform, clip=clip, simplify=simplify)
        self._draw_ps(ps, gc, rgbFace)
