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
