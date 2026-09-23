    def draw_markers(self, gc, marker_path, marker_trans, path, trans,
                     rgbFace=None):
        # docstring inherited

        writeln(self.fh, r"\begin{pgfscope}")

        # convert from display units to in
        f = 1. / self.dpi

        # set style and clip
        self._print_pgf_clip(gc)
        self._print_pgf_path_styles(gc, rgbFace)

        # build marker definition
        bl, tr = marker_path.get_extents(marker_trans).get_points()
        coords = bl[0] * f, bl[1] * f, tr[0] * f, tr[1] * f
        writeln(self.fh,
                r"\pgfsys@defobject{currentmarker}"
                r"{\pgfqpoint{%fin}{%fin}}{\pgfqpoint{%fin}{%fin}}{" % coords)
        self._print_pgf_path(None, marker_path, marker_trans)
        self._pgf_path_draw(stroke=gc.get_linewidth() != 0.0,
                            fill=rgbFace is not None)
        writeln(self.fh, r"}")

        # draw marker for each vertex
        for point, code in path.iter_segments(trans, simplify=False):
            x, y = point[0] * f, point[1] * f
            writeln(self.fh, r"\begin{pgfscope}")
            writeln(self.fh, r"\pgfsys@transformshift{%fin}{%fin}" % (x, y))
            writeln(self.fh, r"\pgfsys@useobject{currentmarker}{}")
            writeln(self.fh, r"\end{pgfscope}")

        writeln(self.fh, r"\end{pgfscope}")
