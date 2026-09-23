    def _process_projection_requirements(
            self, *args, axes_class=None, polar=False, projection=None,
            **kwargs):
        """
        Handle the args/kwargs to add_axes/add_subplot/gca, returning::

            (axes_proj_class, proj_class_kwargs)

        which can be used for new Axes initialization/identification.
        """
        if axes_class is not None:
            if polar or projection is not None:
                raise ValueError(
                    "Cannot combine 'axes_class' and 'projection' or 'polar'")
            projection_class = axes_class
        else:

            if polar:
                if projection is not None and projection != 'polar':
                    raise ValueError(
                        f"polar={polar}, yet projection={projection!r}. "
                        "Only one of these arguments should be supplied."
                    )
                projection = 'polar'

            if isinstance(projection, str) or projection is None:
                projection_class = projections.get_projection_class(projection)
            elif hasattr(projection, '_as_mpl_axes'):
                projection_class, extra_kwargs = projection._as_mpl_axes()
                kwargs.update(**extra_kwargs)
            else:
                raise TypeError(
                    f"projection must be a string, None or implement a "
                    f"_as_mpl_axes method, not {projection!r}")
        return projection_class, kwargs
