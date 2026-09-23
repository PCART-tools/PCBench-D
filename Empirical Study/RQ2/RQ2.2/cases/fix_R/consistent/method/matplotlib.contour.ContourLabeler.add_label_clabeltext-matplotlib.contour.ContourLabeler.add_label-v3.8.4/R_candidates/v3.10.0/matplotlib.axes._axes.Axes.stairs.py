    @_preprocess_data()
    def stairs(self, values, edges=None, *,
               orientation='vertical', baseline=0, fill=False, **kwargs):
        """
        Draw a stepwise constant function as a line or a filled plot.

        *edges* define the x-axis positions of the steps. *values* the function values
        between these steps. Depending on *fill*, the function is drawn either as a
        continuous line with vertical segments at the edges, or as a filled area.

        Parameters
        ----------
        values : array-like
            The step heights.

        edges : array-like
            The step positions, with ``len(edges) == len(vals) + 1``,
            between which the curve takes on vals values.

        orientation : {'vertical', 'horizontal'}, default: 'vertical'
            The direction of the steps. Vertical means that *values* are along
            the y-axis, and edges are along the x-axis.

        baseline : float, array-like or None, default: 0
            The bottom value of the bounding edges or when
            ``fill=True``, position of lower edge. If *fill* is
            True or an array is passed to *baseline*, a closed
            path is drawn.

            If None, then drawn as an unclosed Path.

        fill : bool, default: False
            Whether the area under the step curve should be filled.

            Passing both ``fill=True` and ``baseline=None`` will likely result in
            undesired filling: the first and last points will be connected
            with a straight line and the fill will be between this line and the stairs.


        Returns
        -------
        StepPatch : `~matplotlib.patches.StepPatch`

        Other Parameters
        ----------------
        data : indexable object, optional
            DATA_PARAMETER_PLACEHOLDER

        **kwargs
            `~matplotlib.patches.StepPatch` properties

        """

        if 'color' in kwargs:
            _color = kwargs.pop('color')
        else:
            _color = self._get_lines.get_next_color()
        if fill:
            kwargs.setdefault('linewidth', 0)
            kwargs.setdefault('facecolor', _color)
        else:
            kwargs.setdefault('edgecolor', _color)

        if edges is None:
            edges = np.arange(len(values) + 1)

        edges, values, baseline = self._process_unit_info(
            [("x", edges), ("y", values), ("y", baseline)], kwargs)

        patch = mpatches.StepPatch(values,
                                   edges,
                                   baseline=baseline,
                                   orientation=orientation,
                                   fill=fill,
                                   **kwargs)
        self.add_patch(patch)
        if baseline is None and fill:
            _api.warn_external(
                f"Both {baseline=} and {fill=} have been passed. "
                "baseline=None is only intended for unfilled stair plots. "
                "Because baseline is None, the Path used to draw the stairs will "
                "not be closed, thus because fill is True the polygon will be closed "
                "by drawing an (unstroked) edge from the first to last point.  It is "
                "very likely that the resulting fill patterns is not the desired "
                "result."
            )

        if baseline is not None:
            if orientation == 'vertical':
                patch.sticky_edges.y.append(np.min(baseline))
                self.update_datalim([(edges[0], np.min(baseline))])
            else:
                patch.sticky_edges.x.append(np.min(baseline))
                self.update_datalim([(np.min(baseline), edges[0])])
        self._request_autoscale_view()
        return patch
