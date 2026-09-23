    @_preprocess_data(replace_names=["y", "x1", "x2", "where"],
                      label_namer=None)
    @docstring.dedent_interpd
    def fill_betweenx(self, y, x1, x2=0, where=None,
                      step=None, interpolate=False, **kwargs):
        """
        Make filled polygons between two horizontal curves.


        Create a :class:`~matplotlib.collections.PolyCollection`
        filling the regions between *x1* and *x2* where
        ``where==True``

        Parameters
        ----------
        y : array
            An N-length array of the y data

        x1 : array
            An N-length array (or scalar) of the x data

        x2 : array, optional
            An N-length array (or scalar) of the x data

        where : array, optional
            If *None*, default to fill between everywhere.  If not *None*,
            it is a N length numpy boolean array and the fill will
            only happen over the regions where ``where==True``

        step : {'pre', 'post', 'mid'}, optional
            If not None, fill with step logic.

        interpolate : bool, optional
            If `True`, interpolate between the two lines to find the
            precise point of intersection.  Otherwise, the start and
            end points of the filled region will only occur on explicit
            values in the *x* array.

        Notes
        -----

        keyword args passed on to the
            :class:`~matplotlib.collections.PolyCollection`

        kwargs control the :class:`~matplotlib.patches.Polygon` properties:

        %(PolyCollection)s

        See Also
        --------

            :meth:`fill_between`
                for filling between two sets of y-values

        """

        if not rcParams['_internal.classic_mode']:
            color_aliases = mcoll._color_aliases
            kwargs = cbook.normalize_kwargs(kwargs, color_aliases)

            if not any(c in kwargs for c in ('color', 'facecolors')):
                fc = self._get_patches_for_fill.get_next_color()
                kwargs['facecolors'] = fc
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
        where = where & ~functools.reduce(np.logical_or,
                                          map(np.ma.getmask, [y, x1, x2]))

        y, x1, x2 = np.broadcast_arrays(np.atleast_1d(y), x1, x2)

        polys = []
        for ind0, ind1 in mlab.contiguous_regions(where):
            yslice = y[ind0:ind1]
            x1slice = x1[ind0:ind1]
            x2slice = x2[ind0:ind1]
            if step is not None:
                step_func = STEP_LOOKUP_MAP["steps-" + step]
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
        self.autoscale_view()
        return collection
