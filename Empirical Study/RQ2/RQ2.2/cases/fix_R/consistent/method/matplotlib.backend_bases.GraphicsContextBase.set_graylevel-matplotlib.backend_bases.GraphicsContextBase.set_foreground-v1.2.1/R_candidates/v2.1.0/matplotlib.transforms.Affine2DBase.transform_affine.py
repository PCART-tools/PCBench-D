        def transform_affine(self, points):
            # The major speed trap here is just converting to the
            # points to an array in the first place.  If we can use
            # more arrays upstream, that should help here.
            if not isinstance(points, (np.ma.MaskedArray, np.ndarray)):
                warnings.warn(
                    ('A non-numpy array of type %s was passed in for ' +
                     'transformation.  Please correct this.')
                    % type(points))
            return self._transform_affine(points)
