        def transform_affine(self, values):
            # docstring inherited
            # The major speed trap here is just converting to the
            # points to an array in the first place.  If we can use
            # more arrays upstream, that should help here.
            if not isinstance(values, np.ndarray):
                _api.warn_external(
                    f'A non-numpy array of type {type(values)} was passed in '
                    f'for transformation, which results in poor performance.')
            return self._transform_affine(values)
