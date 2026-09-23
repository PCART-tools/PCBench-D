    def _print_pgf_path(self, gc, path, transform, rgbFace=None):
        f = 1. / self.dpi
        # check for clip box / ignore clip for filled paths
        bbox = gc.get_clip_rectangle() if gc else None
        if bbox and (rgbFace is None):
            p1, p2 = bbox.get_points()
            clip = (p1[0], p1[1], p2[0], p2[1])
        else:
            clip = None
        # build path
        for points, code in path.iter_segments(transform, clip=clip):
            if code == Path.MOVETO:
                x, y = tuple(points)
                writeln(self.fh, r"\pgfpathmoveto{\pgfqpoint{%fin}{%fin}}" %
                        (f * x, f * y))
            elif code == Path.CLOSEPOLY:
                writeln(self.fh, r"\pgfpathclose")
            elif code == Path.LINETO:
                x, y = tuple(points)
                writeln(self.fh, r"\pgfpathlineto{\pgfqpoint{%fin}{%fin}}" %
                        (f * x, f * y))
            elif code == Path.CURVE3:
                cx, cy, px, py = tuple(points)
                coords = cx * f, cy * f, px * f, py * f
                writeln(self.fh, r"\pgfpathquadraticcurveto{\pgfqpoint{%fin}{%fin}}{\pgfqpoint{%fin}{%fin}}" % coords)
            elif code == Path.CURVE4:
                c1x, c1y, c2x, c2y, px, py = tuple(points)
                coords = c1x * f, c1y * f, c2x * f, c2y * f, px * f, py * f
                writeln(self.fh, r"\pgfpathcurveto{\pgfqpoint{%fin}{%fin}}{\pgfqpoint{%fin}{%fin}}{\pgfqpoint{%fin}{%fin}}" % coords)
