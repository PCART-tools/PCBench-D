class Transform(TransformNode):
    """
    The base class of all `TransformNode` instances that
    actually perform a transformation.

    All non-affine transformations should be subclasses of this class.
    New affine transformations should be subclasses of `Affine2D`.

    Subclasses of this class should override the following members (at
    minimum):

    - :attr:`input_dims`
    - :attr:`output_dims`
    - :meth:`transform`
    - :meth:`inverted` (if an inverse exists)

    The following attributes may be overridden if the default is unsuitable:

    - :attr:`is_separable` (defaults to True for 1D -> 1D transforms, False
      otherwise)
    - :attr:`has_inverse` (defaults to True if :meth:`inverted` is overridden,
      False otherwise)

    If the transform needs to do something non-standard with
    `matplotlib.path.Path` objects, such as adding curves
    where there were once line segments, it should override:

    - :meth:`transform_path`
    """

    input_dims = None
    """
    The number of input dimensions of this transform.
    Must be overridden (with integers) in the subclass.
    """

    output_dims = None
    """
    The number of output dimensions of this transform.
    Must be overridden (with integers) in the subclass.
    """

    is_separable = False
    """True if this transform is separable in the x- and y- dimensions."""

    has_inverse = False
    """True if this transform has a corresponding inverse transform."""

    def __init_subclass__(cls):
        # 1d transforms are always separable; we assume higher-dimensional ones
        # are not but subclasses can also directly set is_separable -- this is
        # verified by checking whether "is_separable" appears more than once in
        # the class's MRO (it appears once in Transform).
        if (sum("is_separable" in vars(parent) for parent in cls.__mro__) == 1
                and cls.input_dims == cls.output_dims == 1):
            cls.is_separable = True
        # Transform.inverted raises NotImplementedError; we assume that if this
        # is overridden then the transform is invertible but subclass can also
        # directly set has_inverse.
        if (sum("has_inverse" in vars(parent) for parent in cls.__mro__) == 1
                and hasattr(cls, "inverted")
                and cls.inverted is not Transform.inverted):
            cls.has_inverse = True

    def __add__(self, other):
        """
        Compose two transforms together so that *self* is followed by *other*.

        ``A + B`` returns a transform ``C`` so that
        ``C.transform(x) == B.transform(A.transform(x))``.
        """
        return (composite_transform_factory(self, other)
                if isinstance(other, Transform) else
                NotImplemented)

    # Equality is based on object identity for `Transform`s (so we don't
    # override `__eq__`), but some subclasses, such as TransformWrapper &
    # AffineBase, override this behavior.

    def _iter_break_from_left_to_right(self):
        """
        Return an iterator breaking down this transform stack from left to
        right recursively. If self == ((A, N), A) then the result will be an
        iterator which yields I : ((A, N), A), followed by A : (N, A),
        followed by (A, N) : (A), but not ((A, N), A) : I.

        This is equivalent to flattening the stack then yielding
        ``flat_stack[:i], flat_stack[i:]`` where i=0..(n-1).
        """
        yield IdentityTransform(), self

    @property
    def depth(self):
        """
        Return the number of transforms which have been chained
        together to form this Transform instance.

        .. note::

            For the special case of a Composite transform, the maximum depth
            of the two is returned.

        """
        return 1

    def contains_branch(self, other):
        """
        Return whether the given transform is a sub-tree of this transform.

        This routine uses transform equality to identify sub-trees, therefore
        in many situations it is object id which will be used.

        For the case where the given transform represents the whole
        of this transform, returns True.
        """
        if self.depth < other.depth:
            return False

        # check that a subtree is equal to other (starting from self)
        for _, sub_tree in self._iter_break_from_left_to_right():
            if sub_tree == other:
                return True
        return False

    def contains_branch_seperately(self, other_transform):
        """
        Return whether the given branch is a sub-tree of this transform on
        each separate dimension.

        A common use for this method is to identify if a transform is a blended
        transform containing an Axes' data transform. e.g.::

            x_isdata, y_isdata = trans.contains_branch_seperately(ax.transData)

        """
        if self.output_dims != 2:
            raise ValueError('contains_branch_seperately only supports '
                             'transforms with 2 output dimensions')
        # for a non-blended transform each separate dimension is the same, so
        # just return the appropriate shape.
        return [self.contains_branch(other_transform)] * 2

    def __sub__(self, other):
        """
        Compose *self* with the inverse of *other*, cancelling identical terms
        if any::

            # In general:
            A - B == A + B.inverted()
            # (but see note regarding frozen transforms below).

            # If A "ends with" B (i.e. A == A' + B for some A') we can cancel
            # out B:
            (A' + B) - B == A'

            # Likewise, if B "starts with" A (B = A + B'), we can cancel out A:
            A - (A + B') == B'.inverted() == B'^-1

        Cancellation (rather than naively returning ``A + B.inverted()``) is
        important for multiple reasons:

        - It avoids floating-point inaccuracies when computing the inverse of
          B: ``B - B`` is guaranteed to cancel out exactly (resulting in the
          identity transform), whereas ``B + B.inverted()`` may differ by a
          small epsilon.
        - ``B.inverted()`` always returns a frozen transform: if one computes
          ``A + B + B.inverted()`` and later mutates ``B``, then
          ``B.inverted()`` won't be updated and the last two terms won't cancel
          out anymore; on the other hand, ``A + B - B`` will always be equal to
          ``A`` even if ``B`` is mutated.
        """
        # we only know how to do this operation if other is a Transform.
        if not isinstance(other, Transform):
            return NotImplemented
        for remainder, sub_tree in self._iter_break_from_left_to_right():
            if sub_tree == other:
                return remainder
        for remainder, sub_tree in other._iter_break_from_left_to_right():
            if sub_tree == self:
                if not remainder.has_inverse:
                    raise ValueError(
                        "The shortcut cannot be computed since 'other' "
                        "includes a non-invertible component")
                return remainder.inverted()
        # if we have got this far, then there was no shortcut possible
        if other.has_inverse:
            return self + other.inverted()
        else:
            raise ValueError('It is not possible to compute transA - transB '
                             'since transB cannot be inverted and there is no '
                             'shortcut possible.')

    def __array__(self, *args, **kwargs):
        """Array interface to get at this Transform's affine matrix."""
        return self.get_affine().get_matrix()

    def transform(self, values):
        """
        Apply this transformation on the given array of *values*.

        Parameters
        ----------
        values : array
            The input values as NumPy array of length :attr:`input_dims` or
            shape (N x :attr:`input_dims`).

        Returns
        -------
        array
            The output values as NumPy array of length :attr:`output_dims` or
            shape (N x :attr:`output_dims`), depending on the input.
        """
        # Ensure that values is a 2d array (but remember whether
        # we started with a 1d or 2d array).
        values = np.asanyarray(values)
        ndim = values.ndim
        values = values.reshape((-1, self.input_dims))

        # Transform the values
        res = self.transform_affine(self.transform_non_affine(values))

        # Convert the result back to the shape of the input values.
        if ndim == 0:
            assert not np.ma.is_masked(res)  # just to be on the safe side
            return res[0, 0]
        if ndim == 1:
            return res.reshape(-1)
        elif ndim == 2:
            return res
        raise ValueError(
            "Input values must have shape (N x {dims}) "
            "or ({dims}).".format(dims=self.input_dims))

    def transform_affine(self, values):
        """
        Apply only the affine part of this transformation on the
        given array of values.

        ``transform(values)`` is always equivalent to
        ``transform_affine(transform_non_affine(values))``.

        In non-affine transformations, this is generally a no-op.  In
        affine transformations, this is equivalent to
        ``transform(values)``.

        Parameters
        ----------
        values : array
            The input values as NumPy array of length :attr:`input_dims` or
            shape (N x :attr:`input_dims`).

        Returns
        -------
        array
            The output values as NumPy array of length :attr:`output_dims` or
            shape (N x :attr:`output_dims`), depending on the input.
        """
        return self.get_affine().transform(values)

    def transform_non_affine(self, values):
        """
        Apply only the non-affine part of this transformation.

        ``transform(values)`` is always equivalent to
        ``transform_affine(transform_non_affine(values))``.

        In non-affine transformations, this is generally equivalent to
        ``transform(values)``.  In affine transformations, this is
        always a no-op.

        Parameters
        ----------
        values : array
            The input values as NumPy array of length :attr:`input_dims` or
            shape (N x :attr:`input_dims`).

        Returns
        -------
        array
            The output values as NumPy array of length :attr:`output_dims` or
            shape (N x :attr:`output_dims`), depending on the input.
        """
        return values

    def transform_bbox(self, bbox):
        """
        Transform the given bounding box.

        For smarter transforms including caching (a common requirement in
        Matplotlib), see `TransformedBbox`.
        """
        return Bbox(self.transform(bbox.get_points()))

    def get_affine(self):
        """Get the affine part of this transform."""
        return IdentityTransform()

    def get_matrix(self):
        """Get the matrix for the affine part of this transform."""
        return self.get_affine().get_matrix()

    def transform_point(self, point):
        """
        Return a transformed point.

        This function is only kept for backcompatibility; the more general
        `.transform` method is capable of transforming both a list of points
        and a single point.

        The point is given as a sequence of length :attr:`input_dims`.
        The transformed point is returned as a sequence of length
        :attr:`output_dims`.
        """
        if len(point) != self.input_dims:
            raise ValueError("The length of 'point' must be 'self.input_dims'")
        return self.transform(point)

    def transform_path(self, path):
        """
        Apply the transform to `.Path` *path*, returning a new `.Path`.

        In some cases, this transform may insert curves into the path
        that began as line segments.
        """
        return self.transform_path_affine(self.transform_path_non_affine(path))

    def transform_path_affine(self, path):
        """
        Apply the affine part of this transform to `.Path` *path*, returning a
        new `.Path`.

        ``transform_path(path)`` is equivalent to
        ``transform_path_affine(transform_path_non_affine(values))``.
        """
        return self.get_affine().transform_path_affine(path)

    def transform_path_non_affine(self, path):
        """
        Apply the non-affine part of this transform to `.Path` *path*,
        returning a new `.Path`.

        ``transform_path(path)`` is equivalent to
        ``transform_path_affine(transform_path_non_affine(values))``.
        """
        x = self.transform_non_affine(path.vertices)
        return Path._fast_from_codes_and_verts(x, path.codes, path)

    def transform_angles(self, angles, pts, radians=False, pushoff=1e-5):
        """
        Transform a set of angles anchored at specific locations.

        Parameters
        ----------
        angles : (N,) array-like
            The angles to transform.
        pts : (N, 2) array-like
            The points where the angles are anchored.
        radians : bool, default: False
            Whether *angles* are radians or degrees.
        pushoff : float
            For each point in *pts* and angle in *angles*, the transformed
            angle is computed by transforming a segment of length *pushoff*
            starting at that point and making that angle relative to the
            horizontal axis, and measuring the angle between the horizontal
            axis and the transformed segment.

        Returns
        -------
        (N,) array
        """
        # Must be 2D
        if self.input_dims != 2 or self.output_dims != 2:
            raise NotImplementedError('Only defined in 2D')
        angles = np.asarray(angles)
        pts = np.asarray(pts)
        _api.check_shape((None, 2), pts=pts)
        _api.check_shape((None,), angles=angles)
        if len(angles) != len(pts):
            raise ValueError("There must be as many 'angles' as 'pts'")
        # Convert to radians if desired
        if not radians:
            angles = np.deg2rad(angles)
        # Move a short distance away
        pts2 = pts + pushoff * np.column_stack([np.cos(angles),
                                                np.sin(angles)])
        # Transform both sets of points
        tpts = self.transform(pts)
        tpts2 = self.transform(pts2)
        # Calculate transformed angles
        d = tpts2 - tpts
        a = np.arctan2(d[:, 1], d[:, 0])
        # Convert back to degrees if desired
        if not radians:
            a = np.rad2deg(a)
        return a

    def inverted(self):
        """
        Return the corresponding inverse transformation.

        It holds ``x == self.inverted().transform(self.transform(x))``.

        The return value of this method should be treated as
        temporary.  An update to *self* does not cause a corresponding
        update to its inverted copy.
        """
        raise NotImplementedError()
