    def intersection(self, other):
        """The intersection with another geometrical entity.

        Parameters
        ==========

        o : Point or LinearEntity

        Returns
        =======

        intersection : list of geometrical entities

        See Also
        ========

        sympy.geometry.point.Point

        Examples
        ========

        >>> from sympy import Point, Line, Segment
        >>> p1, p2, p3 = Point(0, 0), Point(1, 1), Point(7, 7)
        >>> l1 = Line(p1, p2)
        >>> l1.intersection(p3)
        [Point2D(7, 7)]
        >>> p4, p5 = Point(5, 0), Point(0, 3)
        >>> l2 = Line(p4, p5)
        >>> l1.intersection(l2)
        [Point2D(15/8, 15/8)]
        >>> p6, p7 = Point(0, 5), Point(2, 6)
        >>> s1 = Segment(p6, p7)
        >>> l1.intersection(s1)
        []
        >>> from sympy import Point3D, Line3D, Segment3D
        >>> p1, p2, p3 = Point3D(0, 0, 0), Point3D(1, 1, 1), Point3D(7, 7, 7)
        >>> l1 = Line3D(p1, p2)
        >>> l1.intersection(p3)
        [Point3D(7, 7, 7)]
        >>> l1 = Line3D(Point3D(4,19,12), Point3D(5,25,17))
        >>> l2 = Line3D(Point3D(-3, -15, -19), direction_ratio=[2,8,8])
        >>> l1.intersection(l2)
        [Point3D(1, 1, -3)]
        >>> p6, p7 = Point3D(0, 5, 2), Point3D(2, 6, 3)
        >>> s1 = Segment3D(p6, p7)
        >>> l1.intersection(s1)
        []

        """
        def intersect_parallel_rays(ray1, ray2):
            if ray1.direction.dot(ray2.direction) > 0:
                # rays point in the same direction
                # so return the one that is "in front"
                return [ray2] if ray1._span_test(ray2.p1) >= 0 else [ray1]
            else:
                # rays point in opposite directions
                st = ray1._span_test(ray2.p1)
                if st < 0:
                    return []
                elif st == 0:
                    return [ray2.p1]
                return [Segment(ray1.p1, ray2.p1)]

        def intersect_parallel_ray_and_segment(ray, seg):
            st1, st2 = ray._span_test(seg.p1), ray._span_test(seg.p2)
            if st1 < 0 and st2 < 0:
                return []
            elif st1 >= 0 and st2 >= 0:
                return [seg]
            elif st1 >= 0:  # st2 < 0:
                return [Segment(ray.p1, seg.p1)]
            else:  # st1 < 0 and st2 >= 0:
                return [Segment(ray.p1, seg.p2)]

        def intersect_parallel_segments(seg1, seg2):
            if seg1.contains(seg2):
                return [seg2]
            if seg2.contains(seg1):
                return [seg1]

            # direct the segments so they're oriented the same way
            if seg1.direction.dot(seg2.direction) < 0:
                seg2 = Segment(seg2.p2, seg2.p1)
            # order the segments so seg1 is "behind" seg2
            if seg1._span_test(seg2.p1) < 0:
                seg1, seg2 = seg2, seg1
            if seg2._span_test(seg1.p2) < 0:
                return []
            return [Segment(seg2.p1, seg1.p2)]

        if not isinstance(other, GeometryEntity):
            other = Point(other, dim=self.ambient_dimension)
        if other.is_Point:
            if self.contains(other):
                return [other]
            else:
                return []
        elif isinstance(other, LinearEntity):
            # break into cases based on whether
            # the lines are parallel, non-parallel intersecting, or skew
            pts = Point._normalize_dimension(self.p1, self.p2, other.p1, other.p2)
            rank = Point.affine_rank(*pts)

            if rank == 1:
                # we're collinear
                if isinstance(self, Line):
                    return [other]
                if isinstance(other, Line):
                    return [self]

                if isinstance(self, Ray) and isinstance(other, Ray):
                    return intersect_parallel_rays(self, other)
                if isinstance(self, Ray) and isinstance(other, Segment):
                    return intersect_parallel_ray_and_segment(self, other)
                if isinstance(self, Segment) and isinstance(other, Ray):
                    return intersect_parallel_ray_and_segment(other, self)
                if isinstance(self, Segment) and isinstance(other, Segment):
                    return intersect_parallel_segments(self, other)
            elif rank == 2:
                # we're in the same plane
                l1 = Line(*pts[:2])
                l2 = Line(*pts[2:])

                # check to see if we're parallel.  If we are, we can't
                # be intersecting, since the collinear case was already
                # handled
                if l1.direction.is_scalar_multiple(l2.direction):
                    return []

                # find the intersection as if everything were lines
                # by solving the equation t*d + p1 == s*d' + p1'
                m = Matrix([l1.direction, -l2.direction]).transpose()
                v = Matrix([l2.p1 - l1.p1]).transpose()

                # we cannot use m.solve(v) because that only works for square matrices
                m_rref, pivots = m.col_insert(2, v).rref(simplify=True)
                # rank == 2 ensures we have 2 pivots, but let's check anyway
                if len(pivots) != 2:
                    raise GeometryError("Failed when solving Mx=b when M={} and b={}".format(m, v))
                coeff = m_rref[0, 2]
                line_intersection = l1.direction*coeff + self.p1

                # if we're both lines, we can skip a containment check
                if isinstance(self, Line) and isinstance(other, Line):
                    return [line_intersection]

                if ((isinstance(self, Line) or
                     self.contains(line_intersection)) and
                        other.contains(line_intersection)):
                    return [line_intersection]
                return []
            else:
                # we're skew
                return []

        return other.intersection(self)
