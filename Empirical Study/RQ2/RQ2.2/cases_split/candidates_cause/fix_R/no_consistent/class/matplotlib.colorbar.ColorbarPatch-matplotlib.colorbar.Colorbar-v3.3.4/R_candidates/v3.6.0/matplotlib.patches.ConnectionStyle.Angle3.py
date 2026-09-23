    @_register_style(_style_list)
    class Angle3(_Base):
        """
        Creates a simple quadratic Bezier curve between two
        points. The middle control points is placed at the
        intersecting point of two lines which cross the start and
        end point, and have a slope of angleA and angleB, respectively.
        """

        def __init__(self, angleA=90, angleB=0):
            """
            *angleA*
              starting angle of the path

            *angleB*
              ending angle of the path
            """

            self.angleA = angleA
            self.angleB = angleB

        def connect(self, posA, posB):
            x1, y1 = posA
            x2, y2 = posB

            cosA = math.cos(math.radians(self.angleA))
            sinA = math.sin(math.radians(self.angleA))
            cosB = math.cos(math.radians(self.angleB))
            sinB = math.sin(math.radians(self.angleB))

            cx, cy = get_intersection(x1, y1, cosA, sinA,
                                      x2, y2, cosB, sinB)

            vertices = [(x1, y1), (cx, cy), (x2, y2)]
            codes = [Path.MOVETO, Path.CURVE3, Path.CURVE3]

            return Path(vertices, codes)
