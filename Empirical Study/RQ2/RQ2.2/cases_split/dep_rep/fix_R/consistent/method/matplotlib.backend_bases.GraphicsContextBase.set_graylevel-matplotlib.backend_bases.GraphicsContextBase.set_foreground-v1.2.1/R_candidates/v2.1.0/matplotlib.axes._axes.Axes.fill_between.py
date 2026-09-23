    @_preprocess_data(replace_names=["x", "y1", "y2", "where"],
                      label_namer=None)
    @docstring.dedent_interpd
    def fill_between(self, x, y1, y2=0, where=None, interpolate=False,
                     step=None,
                     **kwargs):
        """
        Make filled polygons between two curves.


        Create a :class:`~matplotlib.collections.PolyCollection`
        filling the regions between *y1* and *y2* where
        ``where==True``

        Parameters
        ----------
        x : array
            An N-length array of the x data

        y1 : array
            An N-length array (or scalar) of the y data

        y2 : array
            An N-length array (or scalar) of the y data

        where : array, optional
            If `None`, default to fill between everywhere.  If not `None`,
            it is an N-length numpy boolean array and the fill will
            only happen over the regions where ``where==True``.

        interpolate : bool, optional
            If `True`, interpolate between the two lines to find the
            precise point of intersection.  Otherwise, the start and
            end points of the filled region will only occur on explicit
            values in the *x* array.

        step : {'pre', 'post', 'mid'}, optional
            If not None, fill with step logic.


        Notes
        -----

        Additional Keyword args passed on to the
        :class:`~matplotlib.collections.PolyCollection`.

        kwargs control the :class:`~matplotlib.patches.Polygon` properties:

        %(PolyCollection)s

        See Also
        --------

            :meth:`fill_betweenx`
                for filling between two sets of x-values

        """

        if not rcParams['_internal.classic_mode']:
            color_aliases = mcoll._color_aliases
            kwargs = cbook.normalize_kwargs(kwargs, color_aliases)

            if not any(c in kwargs for c in ('color', 'facecolors')):
                fc = self._get_patches_for_fill.get_next_color()
                kwargs['facecolors'] = fc

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
        for ind0, ind1 in mlab.contiguous_regions(where):
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
