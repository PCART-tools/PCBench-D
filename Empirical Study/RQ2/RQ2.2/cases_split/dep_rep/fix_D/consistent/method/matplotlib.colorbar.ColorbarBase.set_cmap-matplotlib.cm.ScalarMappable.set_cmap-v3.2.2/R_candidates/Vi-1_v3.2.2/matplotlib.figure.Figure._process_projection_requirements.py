    def _process_projection_requirements(
            self, *args, polar=False, projection=None, **kwargs):
        """
        Handle the args/kwargs to add_axes/add_subplot/gca, returning::

            (axes_proj_class, proj_class_kwargs, proj_stack_key)

        which can be used for new axes initialization/identification.
        """
        if polar:
            if projection is not None and projection != 'polar':
                raise ValueError(
                    "polar=True, yet projection=%r. "
                    "Only one of these arguments should be supplied." %
                    projection)
            projection = 'polar'

        if isinstance(projection, str) or projection is None:
            projection_class = projections.get_projection_class(projection)
        elif hasattr(projection, '_as_mpl_axes'):
            projection_class, extra_kwargs = projection._as_mpl_axes()
            kwargs.update(**extra_kwargs)
        else:
            raise TypeError('projection must be a string, None or implement a '
                            '_as_mpl_axes method. Got %r' % projection)

        # Make the key without projection kwargs, this is used as a unique
        # lookup for axes instances
        key = self._make_key(*args, **kwargs)

        return projection_class, kwargs, key
