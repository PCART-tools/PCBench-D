    def _fill_between_x_or_y(
            self, ind_dir, ind, dep1, dep2=0, *,
            where=None, interpolate=False, step=None, **kwargs):
        # Common implementation between fill_between (*ind_dir*="x") and
        # fill_betweenx (*ind_dir*="y").  *ind* is the independent variable,
        # *dep* the dependent variable.  The docstring below is interpolated
        # to generate both methods' docstrings.
        """
        Fill the area between two {dir} curves.

        The curves are defined by the points (*{ind}*, *{dep}1*) and (*{ind}*,
        *{dep}2*).  This creates one or multiple polygons describing the filled
        area.

        You may exclude some {dir} sections from filling using *where*.

        By default, the edges connect the given points directly.  Use *step*
        if the filling should be a step function, i.e. constant in between
        *{ind}*.

        Parameters
        ----------
        {ind} : array (length N)
            The {ind} coordinates of the nodes defining the curves.

        {dep}1 : array (length N) or scalar
            The {dep} coordinates of the nodes defining the first curve.

        {dep}2 : array (length N) or scalar, default: 0
            The {dep} coordinates of the nodes defining the second curve.

        where : array of bool (length N), optional
            Define *where* to exclude some {dir} regions from being filled.
            The filled regions are defined by the coordinates ``{ind}[where]``.
            More precisely, fill between ``{ind}[i]`` and ``{ind}[i+1]`` if
            ``where[i] and where[i+1]``.  Note that this definition implies
            that an isolated *True* value between two *False* values in *where*
            will not result in filling.  Both sides of the *True* position
            remain unfilled due to the adjacent *False* values.

        interpolate : bool, default: False
            This option is only relevant if *where* is used and the two curves
            are crossing each other.

            Semantically, *where* is often used for *{dep}1* > *{dep}2* or
            similar.  By default, the nodes of the polygon defining the filled
            region will only be placed at the positions in the *{ind}* array.
            Such a polygon cannot describe the above semantics close to the
            intersection.  The {ind}-sections containing the intersection are
            simply clipped.

            Setting *interpolate* to *True* will calculate the actual
            intersection point and extend the filled region up to this point.

        step : {{'pre', 'post', 'mid'}}, optional
            Define *step* if the filling should be a step function,
            i.e. constant in between *{ind}*.  The value determines where the
            step will occur:

            - 'pre': The {dep} value is continued constantly to the left from
              every *{ind}* position, i.e. the interval ``({ind}[i-1], {ind}[i]]``
              has the value ``{dep}[i]``.
            - 'post': The y value is continued constantly to the right from
              every *{ind}* position, i.e. the interval ``[{ind}[i], {ind}[i+1])``
              has the value ``{dep}[i]``.
            - 'mid': Steps occur half-way between the *{ind}* positions.

        Returns
        -------
        `.FillBetweenPolyCollection`
            A `.FillBetweenPolyCollection` containing the plotted polygons.

        Other Parameters
        ----------------
        data : indexable object, optional
            DATA_PARAMETER_PLACEHOLDER

        **kwargs
            All other keyword arguments are passed on to
            `.FillBetweenPolyCollection`. They control the `.Polygon` properties:

            %(FillBetweenPolyCollection:kwdoc)s

        See Also
        --------
        fill_between : Fill between two sets of y-values.
        fill_betweenx : Fill between two sets of x-values.
        """
        dep_dir = mcoll.FillBetweenPolyCollection._f_dir_from_t(ind_dir)

        if not mpl.rcParams["_internal.classic_mode"]:
            kwargs = cbook.normalize_kwargs(kwargs, mcoll.Collection)
            if not any(c in kwargs for c in ("color", "facecolor")):
                kwargs["facecolor"] = self._get_patches_for_fill.get_next_color()

        ind, dep1, dep2 = self._fill_between_process_units(
            ind_dir, dep_dir, ind, dep1, dep2, **kwargs)

        collection = mcoll.FillBetweenPolyCollection(
            ind_dir, ind, dep1, dep2,
            where=where, interpolate=interpolate, step=step, **kwargs)

        self.add_collection(collection)
        self._request_autoscale_view()
        return collection
