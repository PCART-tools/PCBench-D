    def transform_angles(self, angles, pts, radians=False, pushoff=1e-5):
        """
        Performs transformation on a set of angles anchored at
        specific locations.

        The *angles* must be a column vector (i.e., numpy array).

        The *pts* must be a two-column numpy array of x,y positions
        (angle transforms currently only work in 2D).  This array must
        have the same number of rows as *angles*.

        *radians* indicates whether or not input angles are given in
         radians (True) or degrees (False; the default).

        *pushoff* is the distance to move away from *pts* for
         determining transformed angles (see discussion of method
         below).

        The transformed angles are returned in an array with the same
        size as *angles*.

        The generic version of this method uses a very generic
        algorithm that transforms *pts*, as well as locations very
        close to *pts*, to find the angle in the transformed system.
        """
        # Must be 2D
        if self.input_dims != 2 or self.output_dims != 2:
            raise NotImplementedError('Only defined in 2D')

        if pts.shape[1] != 2:
            raise ValueError("'pts' must be array with 2 columns for x,y")

        if angles.ndim != 1 or angles.shape[0] != pts.shape[0]:
            msg = "'angles' must be a column vector and have same number of"
            msg += " rows as 'pts'"
            raise ValueError(msg)

        # Convert to radians if desired
        if not radians:
            angles = angles / 180.0 * np.pi

        # Move a short distance away
        pts2 = pts + pushoff * np.c_[np.cos(angles), np.sin(angles)]

        # Transform both sets of points
        tpts = self.transform(pts)
        tpts2 = self.transform(pts2)

        # Calculate transformed angles
        d = tpts2 - tpts
        a = np.arctan2(d[:, 1], d[:, 0])

        # Convert back to degrees if desired
        if not radians:
            a = a * 180.0 / np.pi

        return a
