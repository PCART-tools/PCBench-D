    def _get_extension_lengths(self, frac, automin, automax, default=0.05):
        '''
        Get the lengths of colorbar extensions.

        A helper method for _uniform_y and _proportional_y.
        '''
        # Set the default value.
        extendlength = np.array([default, default])
        if isinstance(frac, str):
            if frac.lower() == 'auto':
                # Use the provided values when 'auto' is required.
                extendlength[:] = [automin, automax]
            else:
                # Any other string is invalid.
                raise ValueError('invalid value for extendfrac')
        elif frac is not None:
            try:
                # Try to set min and max extension fractions directly.
                extendlength[:] = frac
                # If frac is a sequence containing None then NaN may
                # be encountered. This is an error.
                if np.isnan(extendlength).any():
                    raise ValueError()
            except (TypeError, ValueError):
                # Raise an error on encountering an invalid value for frac.
                raise ValueError('invalid value for extendfrac')
        return extendlength
