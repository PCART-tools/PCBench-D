    class _Curve(_Base):
        """
        A simple arrow which will work with any path instance. The
        returned path is simply concatenation of the original path + at
        most two paths representing the arrow head at the begin point and the
        at the end point. The arrow heads can be either open or closed.
        """

        def __init__(self, beginarrow=None, endarrow=None,
                     fillbegin=False, fillend=False,
                     head_length=.2, head_width=.1):
            """
            The arrows are drawn if *beginarrow* and/or *endarrow* are
            true. *head_length* and *head_width* determines the size
            of the arrow relative to the *mutation scale*.  The
            arrowhead at the begin (or end) is closed if fillbegin (or
            fillend) is True.
            """
            self.beginarrow, self.endarrow = beginarrow, endarrow
            self.head_length, self.head_width = head_length, head_width
            self.fillbegin, self.fillend = fillbegin, fillend
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

        def transmute(self, path, mutation_size, linewidth):

            head_length = self.head_length * mutation_size
            head_width = self.head_width * mutation_size
            head_dist = np.hypot(head_length, head_width)
            cos_t, sin_t = head_length / head_dist, head_width / head_dist

            # begin arrow
            x0, y0 = path.vertices[0]
            x1, y1 = path.vertices[1]

            # If there is no room for an arrow and a line, then skip the arrow
            has_begin_arrow = self.beginarrow and (x0, y0) != (x1, y1)
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
            has_end_arrow = self.endarrow and (x2, y2) != (x3, y3)
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

            return _path, _fillable
