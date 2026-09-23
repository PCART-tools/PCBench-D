        @staticmethod
        def ensure_quadratic_bezier(path):
            """ Some ArrowStyle class only wokrs with a simple
            quaratic bezier curve (created with Arc3Connetion or
            Angle3Connector). This static method is to check if the
            provided path is a simple quadratic bezier curve and returns
            its control points if true.
            """
            segments = list(path.iter_segments())
            if ((len(segments) != 2) or (segments[0][1] != Path.MOVETO) or
                    (segments[1][1] != Path.CURVE3)):
                msg = "'path' it's not a valid quadratic bezier curve"
                raise ValueError(msg)

            return list(segments[0][0]) + list(segments[1][0])
