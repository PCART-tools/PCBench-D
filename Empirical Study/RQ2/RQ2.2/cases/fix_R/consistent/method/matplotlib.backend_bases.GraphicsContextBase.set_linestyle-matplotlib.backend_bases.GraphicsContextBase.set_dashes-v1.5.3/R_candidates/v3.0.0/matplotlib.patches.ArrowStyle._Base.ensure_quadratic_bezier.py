        @staticmethod
        def ensure_quadratic_bezier(path):
            """
            Some ArrowStyle class only works with a simple quadratic Bezier
            curve (created with Arc3Connetion or Angle3Connector). This static
            method is to check if the provided path is a simple quadratic
            Bezier curve and returns its control points if true.
            """
            segments = list(path.iter_segments())
            if (len(segments) != 2 or segments[0][1] != Path.MOVETO or
                    segments[1][1] != Path.CURVE3):
                raise ValueError(
                    "'path' is not a valid quadratic Bezier curve")
            return [*segments[0][0], *segments[1][0]]
