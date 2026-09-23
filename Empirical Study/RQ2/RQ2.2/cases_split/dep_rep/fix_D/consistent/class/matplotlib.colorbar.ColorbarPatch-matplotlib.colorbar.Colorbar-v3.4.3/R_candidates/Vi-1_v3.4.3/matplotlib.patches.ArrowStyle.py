class ArrowStyle(_Style):
    """
    `ArrowStyle` is a container class which defines several
    arrowstyle classes, which is used to create an arrow path along a
    given path.  These are mainly used with `FancyArrowPatch`.

    A arrowstyle object can be either created as::

           ArrowStyle.Fancy(head_length=.4, head_width=.4, tail_width=.4)

    or::

           ArrowStyle("Fancy", head_length=.4, head_width=.4, tail_width=.4)

    or::

           ArrowStyle("Fancy, head_length=.4, head_width=.4, tail_width=.4")

    The following classes are defined

    %(AvailableArrowstyles)s

    An instance of any arrow style class is a callable object,
    whose call signature is::

        __call__(self, path, mutation_size, linewidth, aspect_ratio=1.)

    and it returns a tuple of a `.Path` instance and a boolean
    value. *path* is a `.Path` instance along which the arrow
    will be drawn. *mutation_size* and *aspect_ratio* have the same
    meaning as in `BoxStyle`. *linewidth* is a line width to be
    stroked. This is meant to be used to correct the location of the
    head so that it does not overshoot the destination point, but not all
    classes support it.
    """

    _style_list = {}

    class _Base:
        """
        Arrow Transmuter Base class

        ArrowTransmuterBase and its derivatives are used to make a fancy
        arrow around a given path. The __call__ method returns a path
        (which will be used to create a PathPatch instance) and a boolean
        value indicating the path is open therefore is not fillable.  This
        class is not an artist and actual drawing of the fancy arrow is
        done by the FancyArrowPatch class.

        """

        # The derived classes are required to be able to be initialized
        # w/o arguments, i.e., all its argument (except self) must have
        # the default values.

        @staticmethod
        def ensure_quadratic_bezier(path):
            """
            Some ArrowStyle class only works with a simple quadratic Bezier
            curve (created with Arc3Connection or Angle3Connector). This static
            method is to check if the provided path is a simple quadratic
            Bezier curve and returns its control points if true.
            """
            segments = list(path.iter_segments())
            if (len(segments) != 2 or segments[0][1] != Path.MOVETO or
                    segments[1][1] != Path.CURVE3):
                raise ValueError(
                    "'path' is not a valid quadratic Bezier curve")
            return [*segments[0][0], *segments[1][0]]

        def transmute(self, path, mutation_size, linewidth):
            """
            The transmute method is the very core of the ArrowStyle class and
            must be overridden in the subclasses. It receives the path object
            along which the arrow will be drawn, and the mutation_size, with
            which the arrow head etc. will be scaled. The linewidth may be
            used to adjust the path so that it does not pass beyond the given
            points. It returns a tuple of a Path instance and a boolean. The
            boolean value indicate whether the path can be filled or not. The
            return value can also be a list of paths and list of booleans of a
            same length.
            """
            raise NotImplementedError('Derived must override')

        def __call__(self, path, mutation_size, linewidth,
                     aspect_ratio=1.):
            """
            The __call__ method is a thin wrapper around the transmute method
            and takes care of the aspect ratio.
            """

            if aspect_ratio is not None:
                # Squeeze the given height by the aspect_ratio
                vertices = path.vertices / [1, aspect_ratio]
                path_shrunk = Path(vertices, path.codes)
                # call transmute method with squeezed height.
                path_mutated, fillable = self.transmute(path_shrunk,
                                                        mutation_size,
                                                        linewidth)
                if np.iterable(fillable):
                    path_list = []
                    for p in path_mutated:
                        # Restore the height
                        path_list.append(
                            Path(p.vertices * [1, aspect_ratio], p.codes))
                    return path_list, fillable
                else:
                    return path_mutated, fillable
            else:
                return self.transmute(path, mutation_size, linewidth)

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

    @_register_style(_style_list, name="-")
    class Curve(_Curve):
        """A simple curve without any arrow head."""

        def __init__(self):
            super().__init__(beginarrow=False, endarrow=False)

    @_register_style(_style_list, name="<-")
    class CurveA(_Curve):
        """An arrow with a head at its begin point."""

        def __init__(self, head_length=.4, head_width=.2):
            """
            Parameters
            ----------
            head_length : float, default: 0.4
                Length of the arrow head.

            head_width : float, default: 0.2
                Width of the arrow head.
            """
            super().__init__(beginarrow=True, endarrow=False,
                             head_length=head_length, head_width=head_width)

    @_register_style(_style_list, name="->")
    class CurveB(_Curve):
        """An arrow with a head at its end point."""

        def __init__(self, head_length=.4, head_width=.2):
            """
            Parameters
            ----------
            head_length : float, default: 0.4
                Length of the arrow head.

            head_width : float, default: 0.2
                Width of the arrow head.
            """
            super().__init__(beginarrow=False, endarrow=True,
                             head_length=head_length, head_width=head_width)

    @_register_style(_style_list, name="<->")
    class CurveAB(_Curve):
        """An arrow with heads both at the begin and the end point."""

        def __init__(self, head_length=.4, head_width=.2):
            """
            Parameters
            ----------
            head_length : float, default: 0.4
                Length of the arrow head.

            head_width : float, default: 0.2
                Width of the arrow head.
            """
            super().__init__(beginarrow=True, endarrow=True,
                             head_length=head_length, head_width=head_width)

    @_register_style(_style_list, name="<|-")
    class CurveFilledA(_Curve):
        """An arrow with filled triangle head at the begin."""

        def __init__(self, head_length=.4, head_width=.2):
            """
            Parameters
            ----------
            head_length : float, default: 0.4
                Length of the arrow head.

            head_width : float, default: 0.2
                Width of the arrow head.
            """
            super().__init__(beginarrow=True, endarrow=False,
                             fillbegin=True, fillend=False,
                             head_length=head_length, head_width=head_width)

    @_register_style(_style_list, name="-|>")
    class CurveFilledB(_Curve):
        """An arrow with filled triangle head at the end."""

        def __init__(self, head_length=.4, head_width=.2):
            """
            Parameters
            ----------
            head_length : float, default: 0.4
                Length of the arrow head.

            head_width : float, default: 0.2
                Width of the arrow head.
            """
            super().__init__(beginarrow=False, endarrow=True,
                             fillbegin=False, fillend=True,
                             head_length=head_length, head_width=head_width)

    @_register_style(_style_list, name="<|-|>")
    class CurveFilledAB(_Curve):
        """An arrow with filled triangle heads at both ends."""

        def __init__(self, head_length=.4, head_width=.2):
            """
            Parameters
            ----------
            head_length : float, default: 0.4
                Length of the arrow head.

            head_width : float, default: 0.2
                Width of the arrow head.
            """
            super().__init__(beginarrow=True, endarrow=True,
                             fillbegin=True, fillend=True,
                             head_length=head_length, head_width=head_width)

    class _Bracket(_Base):

        def __init__(self, bracketA=None, bracketB=None,
                     widthA=1., widthB=1.,
                     lengthA=0.2, lengthB=0.2,
                     angleA=None, angleB=None,
                     scaleA=None, scaleB=None):
            self.bracketA, self.bracketB = bracketA, bracketB
            self.widthA, self.widthB = widthA, widthB
            self.lengthA, self.lengthB = lengthA, lengthB
            self.angleA, self.angleB = angleA, angleB
            self.scaleA, self.scaleB = scaleA, scaleB

        def _get_bracket(self, x0, y0,
                         cos_t, sin_t, width, length, angle):

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

            if angle is not None:
                trans = transforms.Affine2D().rotate_deg_around(x0, y0, angle)
                vertices_arrow = trans.transform(vertices_arrow)

            return vertices_arrow, codes_arrow

        def transmute(self, path, mutation_size, linewidth):

            if self.scaleA is None:
                scaleA = mutation_size
            else:
                scaleA = self.scaleA

            if self.scaleB is None:
                scaleB = mutation_size
            else:
                scaleB = self.scaleB

            vertices_list, codes_list = [], []

            if self.bracketA:
                x0, y0 = path.vertices[0]
                x1, y1 = path.vertices[1]
                cos_t, sin_t = get_cos_sin(x1, y1, x0, y0)
                verticesA, codesA = self._get_bracket(x0, y0, cos_t, sin_t,
                                                      self.widthA * scaleA,
                                                      self.lengthA * scaleA,
                                                      self.angleA)
                vertices_list.append(verticesA)
                codes_list.append(codesA)

            vertices_list.append(path.vertices)
            codes_list.append(path.codes)

            if self.bracketB:
                x0, y0 = path.vertices[-1]
                x1, y1 = path.vertices[-2]
                cos_t, sin_t = get_cos_sin(x1, y1, x0, y0)
                verticesB, codesB = self._get_bracket(x0, y0, cos_t, sin_t,
                                                      self.widthB * scaleB,
                                                      self.lengthB * scaleB,
                                                      self.angleB)
                vertices_list.append(verticesB)
                codes_list.append(codesB)

            vertices = np.concatenate(vertices_list)
            codes = np.concatenate(codes_list)

            p = Path(vertices, codes)

            return p, False

    @_register_style(_style_list, name="]-[")
    class BracketAB(_Bracket):
        """An arrow with outward square brackets at both ends."""

        def __init__(self,
                     widthA=1., lengthA=0.2, angleA=None,
                     widthB=1., lengthB=0.2, angleB=None):
            """
            Parameters
            ----------
            widthA : float, default: 1.0
                Width of the bracket.

            lengthA : float, default: 0.2
                Length of the bracket.

            angleA : float, default: None
                Angle, in degrees, between the bracket and the line. Zero is
                perpendicular to the line, and positive measures
                counterclockwise.

            widthB : float, default: 1.0
                Width of the bracket.

            lengthB : float, default: 0.2
                Length of the bracket.

            angleB : float, default: None
                Angle, in degrees, between the bracket and the line. Zero is
                perpendicular to the line, and positive measures
                counterclockwise.
            """
            super().__init__(True, True,
                             widthA=widthA, lengthA=lengthA, angleA=angleA,
                             widthB=widthB, lengthB=lengthB, angleB=angleB)

    @_register_style(_style_list, name="]-")
    class BracketA(_Bracket):
        """An arrow with an outward square bracket at its start."""

        def __init__(self, widthA=1., lengthA=0.2, angleA=None):
            """
            Parameters
            ----------
            widthA : float, default: 1.0
                Width of the bracket.

            lengthA : float, default: 0.2
                Length of the bracket.

            angleA : float, default: None
                Angle between the bracket and the line.
            """
            super().__init__(True, None,
                             widthA=widthA, lengthA=lengthA, angleA=angleA)

    @_register_style(_style_list, name="-[")
    class BracketB(_Bracket):
        """An arrow with an outward square bracket at its end."""

        def __init__(self, widthB=1., lengthB=0.2, angleB=None):
            """
            Parameters
            ----------
            widthB : float, default: 1.0
                Width of the bracket.

            lengthB : float, default: 0.2
                Length of the bracket.

            angleB : float, default: None
                Angle, in degrees, between the bracket and the line. Zero is
                perpendicular to the line, and positive measures
                counterclockwise.
            """
            super().__init__(None, True,
                             widthB=widthB, lengthB=lengthB, angleB=angleB)

    @_register_style(_style_list, name="|-|")
    class BarAB(_Bracket):
        """An arrow with vertical bars ``|`` at both ends."""

        def __init__(self,
                     widthA=1., angleA=None,
                     widthB=1., angleB=None):
            """
            Parameters
            ----------
            widthA : float, default: 1.0
                Width of the bracket.

            angleA : float, default: None
                Angle, in degrees, between the bracket and the line. Zero is
                perpendicular to the line, and positive measures
                counterclockwise.

            widthB : float, default: 1.0
                Width of the bracket.

            angleB : float, default: None
                Angle, in degrees, between the bracket and the line. Zero is
                perpendicular to the line, and positive measures
                counterclockwise.
            """
            super().__init__(True, True,
                             widthA=widthA, lengthA=0, angleA=angleA,
                             widthB=widthB, lengthB=0, angleB=angleB)

    @_register_style(_style_list)
    class Simple(_Base):
        """A simple arrow. Only works with a quadratic Bezier curve."""

        def __init__(self, head_length=.5, head_width=.5, tail_width=.2):
            """
            Parameters
            ----------
            head_length : float, default: 0.5
                Length of the arrow head.

            head_width : float, default: 0.5
                Width of the arrow head.

            tail_width : float, default: 0.2
                Width of the arrow tail.
            """
            self.head_length, self.head_width, self.tail_width = \
                head_length, head_width, tail_width
            super().__init__()

        def transmute(self, path, mutation_size, linewidth):

            x0, y0, x1, y1, x2, y2 = self.ensure_quadratic_bezier(path)

            # divide the path into a head and a tail
            head_length = self.head_length * mutation_size
            in_f = inside_circle(x2, y2, head_length)
            arrow_path = [(x0, y0), (x1, y1), (x2, y2)]

            try:
                arrow_out, arrow_in = \
                    split_bezier_intersecting_with_closedpath(
                        arrow_path, in_f, tolerance=0.01)
            except NonIntersectingPathException:
                # if this happens, make a straight line of the head_length
                # long.
                x0, y0 = _point_along_a_line(x2, y2, x1, y1, head_length)
                x1n, y1n = 0.5 * (x0 + x2), 0.5 * (y0 + y2)
                arrow_in = [(x0, y0), (x1n, y1n), (x2, y2)]
                arrow_out = None

            # head
            head_width = self.head_width * mutation_size
            head_left, head_right = make_wedged_bezier2(arrow_in,
                                                        head_width / 2., wm=.5)

            # tail
            if arrow_out is not None:
                tail_width = self.tail_width * mutation_size
                tail_left, tail_right = get_parallels(arrow_out,
                                                      tail_width / 2.)

                patch_path = [(Path.MOVETO, tail_right[0]),
                              (Path.CURVE3, tail_right[1]),
                              (Path.CURVE3, tail_right[2]),
                              (Path.LINETO, head_right[0]),
                              (Path.CURVE3, head_right[1]),
                              (Path.CURVE3, head_right[2]),
                              (Path.CURVE3, head_left[1]),
                              (Path.CURVE3, head_left[0]),
                              (Path.LINETO, tail_left[2]),
                              (Path.CURVE3, tail_left[1]),
                              (Path.CURVE3, tail_left[0]),
                              (Path.LINETO, tail_right[0]),
                              (Path.CLOSEPOLY, tail_right[0]),
                              ]
            else:
                patch_path = [(Path.MOVETO, head_right[0]),
                              (Path.CURVE3, head_right[1]),
                              (Path.CURVE3, head_right[2]),
                              (Path.CURVE3, head_left[1]),
                              (Path.CURVE3, head_left[0]),
                              (Path.CLOSEPOLY, head_left[0]),
                              ]

            path = Path([p for c, p in patch_path], [c for c, p in patch_path])

            return path, True

    @_register_style(_style_list)
    class Fancy(_Base):
        """A fancy arrow. Only works with a quadratic Bezier curve."""

        def __init__(self, head_length=.4, head_width=.4, tail_width=.4):
            """
            Parameters
            ----------
            head_length : float, default: 0.4
                Length of the arrow head.

            head_width : float, default: 0.4
                Width of the arrow head.

            tail_width : float, default: 0.4
                Width of the arrow tail.
            """
            self.head_length, self.head_width, self.tail_width = \
                head_length, head_width, tail_width
            super().__init__()

        def transmute(self, path, mutation_size, linewidth):

            x0, y0, x1, y1, x2, y2 = self.ensure_quadratic_bezier(path)

            # divide the path into a head and a tail
            head_length = self.head_length * mutation_size
            arrow_path = [(x0, y0), (x1, y1), (x2, y2)]

            # path for head
            in_f = inside_circle(x2, y2, head_length)
            try:
                path_out, path_in = split_bezier_intersecting_with_closedpath(
                    arrow_path, in_f, tolerance=0.01)
            except NonIntersectingPathException:
                # if this happens, make a straight line of the head_length
                # long.
                x0, y0 = _point_along_a_line(x2, y2, x1, y1, head_length)
                x1n, y1n = 0.5 * (x0 + x2), 0.5 * (y0 + y2)
                arrow_path = [(x0, y0), (x1n, y1n), (x2, y2)]
                path_head = arrow_path
            else:
                path_head = path_in

            # path for head
            in_f = inside_circle(x2, y2, head_length * .8)
            path_out, path_in = split_bezier_intersecting_with_closedpath(
                arrow_path, in_f, tolerance=0.01)
            path_tail = path_out

            # head
            head_width = self.head_width * mutation_size
            head_l, head_r = make_wedged_bezier2(path_head,
                                                 head_width / 2.,
                                                 wm=.6)

            # tail
            tail_width = self.tail_width * mutation_size
            tail_left, tail_right = make_wedged_bezier2(path_tail,
                                                        tail_width * .5,
                                                        w1=1., wm=0.6, w2=0.3)

            # path for head
            in_f = inside_circle(x0, y0, tail_width * .3)
            path_in, path_out = split_bezier_intersecting_with_closedpath(
                arrow_path, in_f, tolerance=0.01)
            tail_start = path_in[-1]

            head_right, head_left = head_r, head_l
            patch_path = [(Path.MOVETO, tail_start),
                          (Path.LINETO, tail_right[0]),
                          (Path.CURVE3, tail_right[1]),
                          (Path.CURVE3, tail_right[2]),
                          (Path.LINETO, head_right[0]),
                          (Path.CURVE3, head_right[1]),
                          (Path.CURVE3, head_right[2]),
                          (Path.CURVE3, head_left[1]),
                          (Path.CURVE3, head_left[0]),
                          (Path.LINETO, tail_left[2]),
                          (Path.CURVE3, tail_left[1]),
                          (Path.CURVE3, tail_left[0]),
                          (Path.LINETO, tail_start),
                          (Path.CLOSEPOLY, tail_start),
                          ]
            path = Path([p for c, p in patch_path], [c for c, p in patch_path])

            return path, True

    @_register_style(_style_list)
    class Wedge(_Base):
        """
        Wedge(?) shape. Only works with a quadratic Bezier curve.  The
        begin point has a width of the tail_width and the end point has a
        width of 0. At the middle, the width is shrink_factor*tail_width.
        """

        def __init__(self, tail_width=.3, shrink_factor=0.5):
            """
            Parameters
            ----------
            tail_width : float, default: 0.3
                Width of the tail.

            shrink_factor : float, default: 0.5
                Fraction of the arrow width at the middle point.
            """
            self.tail_width = tail_width
            self.shrink_factor = shrink_factor
            super().__init__()

        def transmute(self, path, mutation_size, linewidth):

            x0, y0, x1, y1, x2, y2 = self.ensure_quadratic_bezier(path)

            arrow_path = [(x0, y0), (x1, y1), (x2, y2)]
            b_plus, b_minus = make_wedged_bezier2(
                                    arrow_path,
                                    self.tail_width * mutation_size / 2.,
                                    wm=self.shrink_factor)

            patch_path = [(Path.MOVETO, b_plus[0]),
                          (Path.CURVE3, b_plus[1]),
                          (Path.CURVE3, b_plus[2]),
                          (Path.LINETO, b_minus[2]),
                          (Path.CURVE3, b_minus[1]),
                          (Path.CURVE3, b_minus[0]),
                          (Path.CLOSEPOLY, b_minus[0]),
                          ]
            path = Path([p for c, p in patch_path], [c for c, p in patch_path])

            return path, True
