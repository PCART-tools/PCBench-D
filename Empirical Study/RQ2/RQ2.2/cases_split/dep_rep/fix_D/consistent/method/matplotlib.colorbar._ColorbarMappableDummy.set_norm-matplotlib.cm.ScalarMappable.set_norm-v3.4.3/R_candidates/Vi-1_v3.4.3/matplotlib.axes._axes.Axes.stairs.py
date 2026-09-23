    @_preprocess_data()
    def stairs(self, values, edges=None, *,
               orientation='vertical', baseline=0, fill=False, **kwargs):
        """
        A stepwise constant function as a line with bounding edges
        or a filled plot.

        Parameters
        ----------
        values : array-like
            The step heights.

        edges : array-like
            The edge positions, with ``len(edges) == len(vals) + 1``,
            between which the curve takes on vals values.

        orientation : {'vertical', 'horizontal'}, default: 'vertical'
            The direction of the steps. Vertical means that *values* are along
            the y-axis, and edges are along the x-axis.

        baseline : float, array-like or None, default: 0
            The bottom value of the bounding edges or when
            ``fill=True``, position of lower edge. If *fill* is
            True or an array is passed to *baseline*, a closed
            path is drawn.

        fill : bool, default: False
            Whether the area under the step curve should be filled.

        Returns
        -------
        StepPatch : `matplotlib.patches.StepPatch`

        Other Parameters
        ----------------
        **kwargs
            `~matplotlib.patches.StepPatch` properties

        """

        if 'color' in kwargs:
            _color = kwargs.pop('color')
        else:
            _color = self._get_lines.get_next_color()
        if fill:
            kwargs.setdefault('edgecolor', 'none')
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
        if baseline is None:
            baseline = 0
        if orientation == 'vertical':
            patch.sticky_edges.y.append(np.min(baseline))
            self.update_datalim([(edges[0], np.min(baseline))])
        else:
            patch.sticky_edges.x.append(np.min(baseline))
            self.update_datalim([(np.min(baseline), edges[0])])
        self._request_autoscale_view()
        return patch
