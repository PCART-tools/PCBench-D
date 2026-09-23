    @docstring.dedent_interpd
    def gca(self, **kwargs):
        """
        Get the current axes, creating one if necessary

        The following kwargs are supported for ensuring the returned axes
        adheres to the given projection etc., and for axes creation if
        the active axes does not exist:

        %(Axes)s

        """
        ckey, cax = self._axstack.current_key_axes()
        # if there exists an axes on the stack see if it maches
        # the desired axes configuration
        if cax is not None:

            # if no kwargs are given just return the current axes
            # this is a convenience for gca() on axes such as polar etc.
            if not kwargs:
                return cax

            # if the user has specified particular projection detail
            # then build up a key which can represent this
            else:
                # we don't want to modify the original kwargs
                # so take a copy so that we can do what we like to it
                kwargs_copy = kwargs.copy()
                projection_class, _, key = process_projection_requirements(
                    self, **kwargs_copy)

                # let the returned axes have any gridspec by removing it from
                # the key
                ckey = ckey[1:]
                key = key[1:]

                # if the cax matches this key then return the axes, otherwise
                # continue and a new axes will be created
                if key == ckey and isinstance(cax, projection_class):
                    return cax
                else:
                    warnings.warn('Requested projection is different from '
                                  'current axis projection, creating new axis '
                                  'with requested projection.', stacklevel=2)

        # no axes found, so create one which spans the figure
        return self.add_subplot(1, 1, 1, **kwargs)
