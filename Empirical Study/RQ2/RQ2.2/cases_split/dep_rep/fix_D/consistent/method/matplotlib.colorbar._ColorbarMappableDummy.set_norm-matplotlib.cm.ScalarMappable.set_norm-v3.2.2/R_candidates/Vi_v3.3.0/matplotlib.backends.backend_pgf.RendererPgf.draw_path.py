    def draw_path(self, gc, path, transform, rgbFace=None):
        # docstring inherited
        writeln(self.fh, r"\begin{pgfscope}")
        # draw the path
        self._print_pgf_clip(gc)
        self._print_pgf_path_styles(gc, rgbFace)
        self._print_pgf_path(gc, path, transform, rgbFace)
        self._pgf_path_draw(stroke=gc.get_linewidth() != 0.0,
                            fill=rgbFace is not None)
        writeln(self.fh, r"\end{pgfscope}")

        # if present, draw pattern on top
        if gc.get_hatch():
            writeln(self.fh, r"\begin{pgfscope}")
            self._print_pgf_path_styles(gc, rgbFace)

            # combine clip and path for clipping
            self._print_pgf_clip(gc)
            self._print_pgf_path(gc, path, transform, rgbFace)
            writeln(self.fh, r"\pgfusepath{clip}")

            # build pattern definition
            writeln(self.fh,
                    r"\pgfsys@defobject{currentpattern}"
                    r"{\pgfqpoint{0in}{0in}}{\pgfqpoint{1in}{1in}}{")
            writeln(self.fh, r"\begin{pgfscope}")
            writeln(self.fh,
                    r"\pgfpathrectangle"
                    r"{\pgfqpoint{0in}{0in}}{\pgfqpoint{1in}{1in}}")
            writeln(self.fh, r"\pgfusepath{clip}")
            scale = mpl.transforms.Affine2D().scale(self.dpi)
            self._print_pgf_path(None, gc.get_hatch_path(), scale)
            self._pgf_path_draw(stroke=True)
            writeln(self.fh, r"\end{pgfscope}")
            writeln(self.fh, r"}")
            # repeat pattern, filling the bounding rect of the path
            f = 1. / self.dpi
            (xmin, ymin), (xmax, ymax) = \
                path.get_extents(transform).get_points()
            xmin, xmax = f * xmin, f * xmax
            ymin, ymax = f * ymin, f * ymax
            repx, repy = math.ceil(xmax - xmin), math.ceil(ymax - ymin)
            writeln(self.fh,
                    r"\pgfsys@transformshift{%fin}{%fin}" % (xmin, ymin))
            for iy in range(repy):
                for ix in range(repx):
                    writeln(self.fh, r"\pgfsys@useobject{currentpattern}{}")
                    writeln(self.fh, r"\pgfsys@transformshift{1in}{0in}")
                writeln(self.fh, r"\pgfsys@transformshift{-%din}{0in}" % repx)
                writeln(self.fh, r"\pgfsys@transformshift{0in}{1in}")

            writeln(self.fh, r"\end{pgfscope}")
