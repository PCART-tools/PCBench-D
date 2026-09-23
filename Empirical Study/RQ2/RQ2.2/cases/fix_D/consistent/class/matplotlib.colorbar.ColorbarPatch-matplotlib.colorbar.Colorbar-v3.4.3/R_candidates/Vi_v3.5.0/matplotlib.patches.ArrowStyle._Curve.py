    class _Curve(_Base):
        """
        A simple arrow which will work with any path instance. The
        returned path is the concatenation of the original path, and at
        most two paths representing the arrow head or bracket at the begin
        point and at the end point. The arrow heads can be either open
        or closed.
        """

        beginarrow = endarrow = None  # Whether arrows are drawn.
        arrow = "-"
        fillbegin = fillend = False  # Whether arrows are filled.

        def __init__(self, head_length=.4, head_width=.2, widthA=1., widthB=1.,
                     lengthA=0.2, lengthB=0.2, angleA=0, angleB=0, scaleA=None,
                     scaleB=None):
            """
            Parameters
            ----------
            head_length : float, default: 0.4
                Length of the arrow head, relative to *mutation_scale*.
            head_width : float, default: 0.2
                Width of the arrow head, relative to *mutation_scale*.
            widthA : float, default: 1.0
                Width of the bracket at the beginning of the arrow
            widthB : float, default: 1.0
                Width of the bracket at the end of the arrow
            lengthA : float, default: 0.2
                Length of the bracket at the beginning of the arrow
            lengthB : float, default: 0.2
                Length of the bracket at the end of the arrow
            angleA : float, default 0
                Orientation of the bracket at the beginning, as a
                counterclockwise angle. 0 degrees means perpendicular
                to the line.
            angleB : float, default 0
                Orientation of the bracket at the beginning, as a
                counterclockwise angle. 0 degrees means perpendicular
                to the line.
            scaleA : float, default *mutation_size*
                The mutation_size for the beginning bracket
            scaleB : float, default *mutation_size*
                The mutation_size for the end bracket
            """

            self.head_length, self.head_width = head_length, head_width
            self.widthA, self.widthB = widthA, widthB
            self.lengthA, self.lengthB = lengthA, lengthB
            self.angleA, self.angleB = angleA, angleB
            self.scaleA, self.scaleB = scaleA, scaleB

            self._beginarrow_head = False
            self._beginarrow_bracket = False
            self._endarrow_head = False
            self._endarrow_bracket = False

            if "-" not in self.arrow:
                raise ValueError("arrow must have the '-' between "
                                 "the two heads")

            beginarrow, endarrow = self.arrow.split("-", 1)

            if beginarrow == "<":
                self._beginarrow_head = True
                self._beginarrow_bracket = False
            elif beginarrow == "<|":
                self._beginarrow_head = True
                self._beginarrow_bracket = False
                self.fillbegin = True
            elif beginarrow in ("]", "|"):
                self._beginarrow_head = False
                self._beginarrow_bracket = True
            elif self.beginarrow is True:
                self._beginarrow_head = True
                self._beginarrow_bracket = False

                _api.warn_deprecated('3.5', name="beginarrow",
                                     alternative="arrow")
            elif self.beginarrow is False:
                self._beginarrow_head = False
                self._beginarrow_bracket = False

                _api.warn_deprecated('3.5', name="beginarrow",
                                     alternative="arrow")

            if endarrow == ">":
                self._endarrow_head = True
                self._endarrow_bracket = False
            elif endarrow == "|>":
                self._endarrow_head = True
                self._endarrow_bracket = False
                self.fillend = True
            elif endarrow in ("[", "|"):
                self._endarrow_head = False
                self._endarrow_bracket = True
            elif self.endarrow is True:
                self._endarrow_head = True
                self._endarrow_bracket = False

                _api.warn_deprecated('3.5', name="endarrow",
                                     alternative="arrow")
            elif self.endarrow is False:
                self._endarrow_head = False
                self._endarrow_bracket = False

                _api.warn_deprecated('3.5', name="endarrow",
                                     alternative="arrow")

            super().__init__()

        def _get_arrow_wedge(self, x0, y0, x1, y1,
                             head_dist, cos_t, sin_t, linewidth):
            """
            Return the paths for arrow heads. Since arrow lines are
            drawn with capstyle=projected, The arrow goes beyond the
            desired point. This method also returns the amount of the path
            to be shrunken so that it does not overshoot.
            """

            # arrow from x0, y0 to x1, y1
            dx, dy = x0 - x1, y0 - y1

            cp_distance = np.hypot(dx, dy)

            # pad_projected : amount of pad to account the
            # overshooting of the projection of the wedge
            pad_projected = (.5 * linewidth / sin_t)

            # Account for division by zero
            if cp_distance == 0:
                cp_distance = 1

            # apply pad for projected edge
            ddx = pad_projected * dx / cp_distance
            ddy = pad_projected * dy / cp_distance

            # offset for arrow wedge
            dx = dx / cp_distance * head_dist
            dy = dy / cp_distance * head_dist

            dx1, dy1 = cos_t * dx + sin_t * dy, -sin_t * dx + cos_t * dy
            dx2, dy2 = cos_t * dx - sin_t * dy, sin_t * dx + cos_t * dy

            vertices_arrow = [(x1 + ddx + dx1, y1 + ddy + dy1),
                              (x1 + ddx, y1 + ddy),
                              (x1 + ddx + dx2, y1 + ddy + dy2)]
            codes_arrow = [Path.MOVETO,
                           Path.LINETO,
                           Path.LINETO]

            return vertices_arrow, codes_arrow, ddx, ddy

        def _get_bracket(self, x0, y0,
                         x1, y1, width, length, angle):

            cos_t, sin_t = get_cos_sin(x1, y1, x0, y0)

            # arrow from x0, y0 to x1, y1
            from matplotlib.bezier import get_normal_points
            x1, y1, x2, y2 = get_normal_points(x0, y0, cos_t, sin_t, width)

            dx, dy = length * cos_t, length * sin_t

            vertices_arrow = [(x1 + dx, y1 + dy),
                              (x1, y1),
                              (x2, y2),
                              (x2 + dx, y2 + dy)]
            codes_arrow = [Path.MOVETO,
                           Path.LINETO,
                           Path.LINETO,
                           Path.LINETO]

            if angle:
                trans = transforms.Affine2D().rotate_deg_around(x0, y0, angle)
                vertices_arrow = trans.transform(vertices_arrow)

            return vertices_arrow, codes_arrow

        def transmute(self, path, mutation_size, linewidth):

            if self._beginarrow_head or self._endarrow_head:
                head_length = self.head_length * mutation_size
                head_width = self.head_width * mutation_size
                head_dist = np.hypot(head_length, head_width)
                cos_t, sin_t = head_length / head_dist, head_width / head_dist

            scaleA = mutation_size if self.scaleA is None else self.scaleA
            scaleB = mutation_size if self.scaleB is None else self.scaleB

            # begin arrow
            x0, y0 = path.vertices[0]
            x1, y1 = path.vertices[1]

            # If there is no room for an arrow and a line, then skip the arrow
            has_begin_arrow = self._beginarrow_head and (x0, y0) != (x1, y1)
            verticesA, codesA, ddxA, ddyA = (
                self._get_arrow_wedge(x1, y1, x0, y0,
                                      head_dist, cos_t, sin_t, linewidth)
                if has_begin_arrow
                else ([], [], 0, 0)
            )

            # end arrow
            x2, y2 = path.vertices[-2]
            x3, y3 = path.vertices[-1]

            # If there is no room for an arrow and a line, then skip the arrow
            has_end_arrow = self._endarrow_head and (x2, y2) != (x3, y3)
            verticesB, codesB, ddxB, ddyB = (
                self._get_arrow_wedge(x2, y2, x3, y3,
                                      head_dist, cos_t, sin_t, linewidth)
                if has_end_arrow
                else ([], [], 0, 0)
            )

            # This simple code will not work if ddx, ddy is greater than the
            # separation between vertices.
            _path = [Path(np.concatenate([[(x0 + ddxA, y0 + ddyA)],
                                          path.vertices[1:-1],
                                          [(x3 + ddxB, y3 + ddyB)]]),
                          path.codes)]
            _fillable = [False]

            if has_begin_arrow:
                if self.fillbegin:
                    p = np.concatenate([verticesA, [verticesA[0],
                                                    verticesA[0]], ])
                    c = np.concatenate([codesA, [Path.LINETO, Path.CLOSEPOLY]])
                    _path.append(Path(p, c))
                    _fillable.append(True)
                else:
                    _path.append(Path(verticesA, codesA))
                    _fillable.append(False)
            elif self._beginarrow_bracket:
                x0, y0 = path.vertices[0]
                x1, y1 = path.vertices[1]
                verticesA, codesA = self._get_bracket(x0, y0, x1, y1,
                                                      self.widthA * scaleA,
                                                      self.lengthA * scaleA,
                                                      self.angleA)

                _path.append(Path(verticesA, codesA))
                _fillable.append(False)

            if has_end_arrow:
                if self.fillend:
                    _fillable.append(True)
                    p = np.concatenate([verticesB, [verticesB[0],
                                                    verticesB[0]], ])
                    c = np.concatenate([codesB, [Path.LINETO, Path.CLOSEPOLY]])
                    _path.append(Path(p, c))
                else:
                    _fillable.append(False)
                    _path.append(Path(verticesB, codesB))
            elif self._endarrow_bracket:
                x0, y0 = path.vertices[-1]
                x1, y1 = path.vertices[-2]
                verticesB, codesB = self._get_bracket(x0, y0, x1, y1,
                                                      self.widthB * scaleB,
                                                      self.lengthB * scaleB,
                                                      self.angleB)

                _path.append(Path(verticesB, codesB))
                _fillable.append(False)

            return _path, _fillable
