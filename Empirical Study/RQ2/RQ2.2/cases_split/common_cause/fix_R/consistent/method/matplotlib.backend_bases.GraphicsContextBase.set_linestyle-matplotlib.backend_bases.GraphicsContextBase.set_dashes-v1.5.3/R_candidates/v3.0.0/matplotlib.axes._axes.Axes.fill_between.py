    @_preprocess_data(replace_names=["x", "y1", "y2", "where"],
                      label_namer=None)
    @docstring.dedent_interpd
    def fill_between(self, x, y1, y2=0, where=None, interpolate=False,
                     step=None, **kwargs):
        """
        Fill the area between two horizontal curves.

        The curves are defined by the points (*x*, *y1*) and (*x*, *y2*). This
        creates one or multiple polygons describing the filled area.

        You may exclude some horizontal sections from filling using *where*.

        By default, the edges connect the given points directly. Use *step* if
        the filling should be a step function, i.e. constant in between *x*.


        Parameters
        ----------
        x : array (length N)
            The x coordinates of the nodes defining the curves.

        y1 : array (length N) or scalar
            The y coordinates of the nodes defining the first curve.

        y2 : array (length N) or scalar, optional, default: 0
            The y coordinates of the nodes defining the second curve.

        where : array of bool (length N), optional, default: None
            Define *where* to exclude some horizontal regions from being
            filled. The filled regions are defined by the coordinates
            ``x[where]``.  More precisely, fill between ``x[i]`` and ``x[i+1]``
            if ``where[i] and where[i+1]``.  Note that this definition implies
            that an isolated *True* value between two *False* values in
            *where* will not result in filling.  Both sides of the *True*
            position remain unfilled due to the adjacent *False* values.

        interpolate : bool, optional
            This option is only relvant if *where* is used and the two curves
            are crossing each other.

            Semantically, *where* is often used for *y1* > *y2* or similar.
            By default, the nodes of the polygon defining the filled region
            will only be placed at the positions in the *x* array.  Such a
            polygon cannot describe the above semantics close to the
            intersection.  The x-sections containing the intersection are
            simply clipped.

            Setting *interpolate* to *True* will calculate the actual
            intersection point and extend the filled region up to this point.

        step : {'pre', 'post', 'mid'}, optional
            Define *step* if the filling should be a step function,
            i.e. constant in between *x*. The value determines where the
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
        fill_betweenx : Fill between two sets of x-values.

        Notes
        -----
        .. [notes section required to get data note injection right]

        """
        if not rcParams['_internal.classic_mode']:
            kwargs = cbook.normalize_kwargs(
                kwargs, mcoll.Collection._alias_map)
            if not any(c in kwargs for c in ('color', 'facecolor')):
                kwargs['facecolor'] = \
                    self._get_patches_for_fill.get_next_color()

        # Handle united data, such as dates
        self._process_unit_info(xdata=x, ydata=y1, kwargs=kwargs)
        self._process_unit_info(ydata=y2)

        # Convert the arrays so we can work with them
        x = ma.masked_invalid(self.convert_xunits(x))
        y1 = ma.masked_invalid(self.convert_yunits(y1))
        y2 = ma.masked_invalid(self.convert_yunits(y2))

        for name, array in [('x', x), ('y1', y1), ('y2', y2)]:
            if array.ndim > 1:
                raise ValueError('Input passed into argument "%r"' % name +
                                 'is not 1-dimensional.')

        if where is None:
            where = True
        where = where & ~functools.reduce(np.logical_or,
                                          map(np.ma.getmask, [x, y1, y2]))

        x, y1, y2 = np.broadcast_arrays(np.atleast_1d(x), y1, y2)

        polys = []
        for ind0, ind1 in cbook.contiguous_regions(where):
            xslice = x[ind0:ind1]
            y1slice = y1[ind0:ind1]
            y2slice = y2[ind0:ind1]
            if step is not None:
                step_func = STEP_LOOKUP_MAP["steps-" + step]
                xslice, y1slice, y2slice = step_func(xslice, y1slice, y2slice)

            if not len(xslice):
                continue

            N = len(xslice)
            X = np.zeros((2 * N + 2, 2), float)

            if interpolate:
                def get_interp_point(ind):
                    im1 = max(ind - 1, 0)
                    x_values = x[im1:ind + 1]
                    diff_values = y1[im1:ind + 1] - y2[im1:ind + 1]
                    y1_values = y1[im1:ind + 1]

                    if len(diff_values) == 2:
                        if np.ma.is_masked(diff_values[1]):
                            return x[im1], y1[im1]
                        elif np.ma.is_masked(diff_values[0]):
                            return x[ind], y1[ind]

                    diff_order = diff_values.argsort()
                    diff_root_x = np.interp(
                        0, diff_values[diff_order], x_values[diff_order])
                    x_order = x_values.argsort()
                    diff_root_y = np.interp(diff_root_x, x_values[x_order],
                                            y1_values[x_order])
                    return diff_root_x, diff_root_y

                start = get_interp_point(ind0)
                end = get_interp_point(ind1)
            else:
                # the purpose of the next two lines is for when y2 is a
                # scalar like 0 and we want the fill to go all the way
                # down to 0 even if none of the y1 sample points do
                start = xslice[0], y2slice[0]
                end = xslice[-1], y2slice[-1]

            X[0] = start
            X[N + 1] = end

            X[1:N + 1, 0] = xslice
            X[1:N + 1, 1] = y1slice
            X[N + 2:, 0] = xslice[::-1]
            X[N + 2:, 1] = y2slice[::-1]

            polys.append(X)

        collection = mcoll.PolyCollection(polys, **kwargs)

        # now update the datalim and autoscale
        XY1 = np.array([x[where], y1[where]]).T
        XY2 = np.array([x[where], y2[where]]).T
        self.dataLim.update_from_data_xy(XY1, self.ignore_existing_data_limits,
                                         updatex=True, updatey=True)
        self.ignore_existing_data_limits = False
        self.dataLim.update_from_data_xy(XY2, self.ignore_existing_data_limits,
                                         updatex=False, updatey=True)
        self.add_collection(collection, autolim=False)
        self.autoscale_view()
        return collection
