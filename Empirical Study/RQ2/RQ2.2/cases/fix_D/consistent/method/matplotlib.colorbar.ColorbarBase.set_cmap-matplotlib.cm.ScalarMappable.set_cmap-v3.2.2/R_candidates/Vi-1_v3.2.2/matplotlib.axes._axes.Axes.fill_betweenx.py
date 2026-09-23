    @_preprocess_data(replace_names=["y", "x1", "x2", "where"])
    @docstring.dedent_interpd
    def fill_betweenx(self, y, x1, x2=0, where=None,
                      step=None, interpolate=False, **kwargs):
        """
        Fill the area between two vertical curves.

        The curves are defined by the points (*x1*, *y*) and (*x2*, *y*). This
        creates one or multiple polygons describing the filled area.

        You may exclude some vertical sections from filling using *where*.

        By default, the edges connect the given points directly. Use *step* if
        the filling should be a step function, i.e. constant in between *y*.


        Parameters
        ----------
        y : array (length N)
            The y coordinates of the nodes defining the curves.

        x1 : array (length N) or scalar
            The x coordinates of the nodes defining the first curve.

        x2 : array (length N) or scalar, optional, default: 0
            The x coordinates of the nodes defining the second curve.

        where : array of bool (length N), optional, default: None
            Define *where* to exclude some vertical regions from being
            filled. The filled regions are defined by the coordinates
            ``y[where]``.  More precisely, fill between ``y[i]`` and ``y[i+1]``
            if ``where[i] and where[i+1]``.  Note that this definition implies
            that an isolated *True* value between two *False* values in
            *where* will not result in filling.  Both sides of the *True*
            position remain unfilled due to the adjacent *False* values.

        interpolate : bool, optional
            This option is only relevant if *where* is used and the two curves
            are crossing each other.

            Semantically, *where* is often used for *x1* > *x2* or similar.
            By default, the nodes of the polygon defining the filled region
            will only be placed at the positions in the *y* array.  Such a
            polygon cannot describe the above semantics close to the
            intersection.  The y-sections containing the intersection are
            simply clipped.

            Setting *interpolate* to *True* will calculate the actual
            intersection point and extend the filled region up to this point.

        step : {'pre', 'post', 'mid'}, optional
            Define *step* if the filling should be a step function,
            i.e. constant in between *y*. The value determines where the
            step will occur:

            - 'pre': The y value is continued constantly to the left from
              every *x* position, i.e. the interval ``(x[i-1], x[i]]`` has the
              value ``y[i]``.
            - 'post': The y value is continued constantly to the right from
              every *x* position, i.e. the interval ``[x[i], x[i+1])`` has the
              value ``y[i]``.
            - 'mid': Steps occur half-way between the *x* positions.

        Other Parameters
        ----------------
        **kwargs
            All other keyword arguments are passed on to `.PolyCollection`.
            They control the `.Polygon` properties:

            %(PolyCollection)s

        Returns
        -------
        `.PolyCollection`
            A `.PolyCollection` containing the plotted polygons.

        See Also
        --------
        fill_between : Fill between two sets of y-values.

        Notes
        -----
        .. [notes section required to get data note injection right]

        """
        if not rcParams['_internal.classic_mode']:
            kwargs = cbook.normalize_kwargs(kwargs, mcoll.Collection)
            if not any(c in kwargs for c in ('color', 'facecolor')):
                kwargs['facecolor'] = \
                    self._get_patches_for_fill.get_next_color()

        # Handle united data, such as dates
        self._process_unit_info(ydata=y, xdata=x1, kwargs=kwargs)
        self._process_unit_info(xdata=x2)

        # Convert the arrays so we can work with them
        y = ma.masked_invalid(self.convert_yunits(y))
        x1 = ma.masked_invalid(self.convert_xunits(x1))
        x2 = ma.masked_invalid(self.convert_xunits(x2))

        for name, array in [('y', y), ('x1', x1), ('x2', x2)]:
            if array.ndim > 1:
                raise ValueError('Input passed into argument "%r"' % name +
                                 'is not 1-dimensional.')

        if where is None:
            where = True
        else:
            where = np.asarray(where, dtype=bool)
            if where.size != y.size:
                cbook.warn_deprecated(
                    "3.2",
                    message="The parameter where must have the same size as y "
                            "in fill_between(). This will become an error in "
                            "future versions of Matplotlib.")
        where = where & ~functools.reduce(np.logical_or,
                                          map(np.ma.getmask, [y, x1, x2]))

        y, x1, x2 = np.broadcast_arrays(np.atleast_1d(y), x1, x2)

        polys = []
        for ind0, ind1 in cbook.contiguous_regions(where):
            yslice = y[ind0:ind1]
            x1slice = x1[ind0:ind1]
            x2slice = x2[ind0:ind1]
            if step is not None:
                step_func = cbook.STEP_LOOKUP_MAP["steps-" + step]
                yslice, x1slice, x2slice = step_func(yslice, x1slice, x2slice)

            if not len(yslice):
                continue

            N = len(yslice)
            Y = np.zeros((2 * N + 2, 2), float)
            if interpolate:
                def get_interp_point(ind):
                    im1 = max(ind - 1, 0)
                    y_values = y[im1:ind + 1]
                    diff_values = x1[im1:ind + 1] - x2[im1:ind + 1]
                    x1_values = x1[im1:ind + 1]

                    if len(diff_values) == 2:
                        if np.ma.is_masked(diff_values[1]):
                            return x1[im1], y[im1]
                        elif np.ma.is_masked(diff_values[0]):
                            return x1[ind], y[ind]

                    diff_order = diff_values.argsort()
                    diff_root_y = np.interp(
                        0, diff_values[diff_order], y_values[diff_order])
                    y_order = y_values.argsort()
                    diff_root_x = np.interp(diff_root_y, y_values[y_order],
                                            x1_values[y_order])
                    return diff_root_x, diff_root_y

                start = get_interp_point(ind0)
                end = get_interp_point(ind1)
            else:
                # the purpose of the next two lines is for when x2 is a
                # scalar like 0 and we want the fill to go all the way
                # down to 0 even if none of the x1 sample points do
                start = x2slice[0], yslice[0]
                end = x2slice[-1], yslice[-1]

            Y[0] = start
            Y[N + 1] = end

            Y[1:N + 1, 0] = x1slice
            Y[1:N + 1, 1] = yslice
            Y[N + 2:, 0] = x2slice[::-1]
            Y[N + 2:, 1] = yslice[::-1]

            polys.append(Y)

        collection = mcoll.PolyCollection(polys, **kwargs)

        # now update the datalim and autoscale
        X1Y = np.array([x1[where], y[where]]).T
        X2Y = np.array([x2[where], y[where]]).T
        self.dataLim.update_from_data_xy(X1Y, self.ignore_existing_data_limits,
                                         updatex=True, updatey=True)
        self.ignore_existing_data_limits = False
        self.dataLim.update_from_data_xy(X2Y, self.ignore_existing_data_limits,
                                         updatex=True, updatey=False)
        self.add_collection(collection, autolim=False)
        self._request_autoscale_view()
        return collection
