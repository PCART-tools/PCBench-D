    def _print_pgf_path(self, gc, path, transform, rgbFace=None):
        f = 1. / self.dpi
        # check for clip box / ignore clip for filled paths
        bbox = gc.get_clip_rectangle() if gc else None
        maxcoord = 16383 / 72.27 * self.dpi  # Max dimensions in LaTeX.
        if bbox and (rgbFace is None):
            p1, p2 = bbox.get_points()
            clip = (max(p1[0], -maxcoord), max(p1[1], -maxcoord),
                    min(p2[0], maxcoord), min(p2[1], maxcoord))
        else:
            clip = (-maxcoord, -maxcoord, maxcoord, maxcoord)
        # build path
        for points, code in path.iter_segments(transform, clip=clip):
            if code == Path.MOVETO:
                x, y = tuple(points)
                _writeln(self.fh,
                         r"\pgfpathmoveto{\pgfqpoint{%fin}{%fin}}" %
                         (f * x, f * y))
            elif code == Path.CLOSEPOLY:
                _writeln(self.fh, r"\pgfpathclose")
            elif code == Path.LINETO:
                x, y = tuple(points)
                _writeln(self.fh,
                         r"\pgfpathlineto{\pgfqpoint{%fin}{%fin}}" %
                         (f * x, f * y))
            elif code == Path.CURVE3:
                cx, cy, px, py = tuple(points)
                coords = cx * f, cy * f, px * f, py * f
                _writeln(self.fh,
                         r"\pgfpathquadraticcurveto"
                         r"{\pgfqpoint{%fin}{%fin}}{\pgfqpoint{%fin}{%fin}}"
                         % coords)
            elif code == Path.CURVE4:
                c1x, c1y, c2x, c2y, px, py = tuple(points)
                coords = c1x * f, c1y * f, c2x * f, c2y * f, px * f, py * f
                _writeln(self.fh,
                         r"\pgfpathcurveto"
                         r"{\pgfqpoint{%fin}{%fin}}"
                         r"{\pgfqpoint{%fin}{%fin}}"
                         r"{\pgfqpoint{%fin}{%fin}}"
                         % coords)

        # apply pgf decorators
        sketch_params = gc.get_sketch_params() if gc else None
        if sketch_params is not None:
            # Only "length" directly maps to "segment length" in PGF's API.
            # PGF uses "amplitude" to pass the combined deviation in both x-
            # and y-direction, while matplotlib only varies the length of the
            # wiggle along the line ("randomness" and "length" parameters)
            # and has a separate "scale" argument for the amplitude.
            # -> Use "randomness" as PRNG seed to allow the user to force the
            # same shape on multiple sketched lines
            scale, length, randomness = sketch_params
            if scale is not None:
                # make matplotlib and PGF rendering visually similar
                length *= 0.5
                scale *= 2
                # PGF guarantees that repeated loading is a no-op
                _writeln(self.fh, r"\usepgfmodule{decorations}")
                _writeln(self.fh, r"\usepgflibrary{decorations.pathmorphing}")
                _writeln(self.fh, r"\pgfkeys{/pgf/decoration/.cd, "
                         f"segment length = {(length * f):f}in, "
                         f"amplitude = {(scale * f):f}in}}")
                _writeln(self.fh, f"\\pgfmathsetseed{{{int(randomness)}}}")
                _writeln(self.fh, r"\pgfdecoratecurrentpath{random steps}")
