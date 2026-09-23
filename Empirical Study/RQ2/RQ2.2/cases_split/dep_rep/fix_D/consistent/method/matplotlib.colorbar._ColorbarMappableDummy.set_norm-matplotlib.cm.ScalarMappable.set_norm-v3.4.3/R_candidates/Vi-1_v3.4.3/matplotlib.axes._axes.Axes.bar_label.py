    def bar_label(self, container, labels=None, *, fmt="%g", label_type="edge",
                  padding=0, **kwargs):
        """
        Label a bar plot.

        Adds labels to bars in the given `.BarContainer`.
        You may need to adjust the axis limits to fit the labels.

        Parameters
        ----------
        container : `.BarContainer`
            Container with all the bars and optionally errorbars, likely
            returned from `.bar` or `.barh`.

        labels : array-like, optional
            A list of label texts, that should be displayed. If not given, the
            label texts will be the data values formatted with *fmt*.

        fmt : str, default: '%g'
            A format string for the label.

        label_type : {'edge', 'center'}, default: 'edge'
            The label type. Possible values:

            - 'edge': label placed at the end-point of the bar segment, and the
              value displayed will be the position of that end-point.
            - 'center': label placed in the center of the bar segment, and the
              value displayed will be the length of that segment.
              (useful for stacked bars, i.e.,
              :doc:`/gallery/lines_bars_and_markers/bar_label_demo`)

        padding : float, default: 0
            Distance of label from the end of the bar, in points.

        **kwargs
            Any remaining keyword arguments are passed through to
            `.Axes.annotate`.

        Returns
        -------
        list of `.Text`
            A list of `.Text` instances for the labels.
        """

        # want to know whether to put label on positive or negative direction
        # cannot use np.sign here because it will return 0 if x == 0
        def sign(x):
            return 1 if x >= 0 else -1

        _api.check_in_list(['edge', 'center'], label_type=label_type)

        bars = container.patches
        errorbar = container.errorbar
        datavalues = container.datavalues
        orientation = container.orientation

        if errorbar:
            # check "ErrorbarContainer" for the definition of these elements
            lines = errorbar.lines  # attribute of "ErrorbarContainer" (tuple)
            barlinecols = lines[2]  # 0: data_line, 1: caplines, 2: barlinecols
            barlinecol = barlinecols[0]  # the "LineCollection" of error bars
            errs = barlinecol.get_segments()
        else:
            errs = []

        if labels is None:
            labels = []

        annotations = []

        for bar, err, dat, lbl in itertools.zip_longest(
            bars, errs, datavalues, labels
        ):
            (x0, y0), (x1, y1) = bar.get_bbox().get_points()
            xc, yc = (x0 + x1) / 2, (y0 + y1) / 2

            if orientation == "vertical":
                extrema = max(y0, y1) if dat >= 0 else min(y0, y1)
                length = abs(y0 - y1)
            elif orientation == "horizontal":
                extrema = max(x0, x1) if dat >= 0 else min(x0, x1)
                length = abs(x0 - x1)

            if err is None:
                endpt = extrema
            elif orientation == "vertical":
                endpt = err[:, 1].max() if dat >= 0 else err[:, 1].min()
            elif orientation == "horizontal":
                endpt = err[:, 0].max() if dat >= 0 else err[:, 0].min()

            if label_type == "center":
                value = sign(dat) * length
            elif label_type == "edge":
                value = extrema

            if label_type == "center":
                xy = xc, yc
            elif label_type == "edge" and orientation == "vertical":
                xy = xc, endpt
            elif label_type == "edge" and orientation == "horizontal":
                xy = endpt, yc

            if orientation == "vertical":
                xytext = 0, sign(dat) * padding
            else:
                xytext = sign(dat) * padding, 0

            if label_type == "center":
                ha, va = "center", "center"
            elif label_type == "edge":
                if orientation == "vertical":
                    ha = 'center'
                    va = 'top' if dat < 0 else 'bottom'  # also handles NaN
                elif orientation == "horizontal":
                    ha = 'right' if dat < 0 else 'left'  # also handles NaN
                    va = 'center'

            if np.isnan(dat):
                lbl = ''

            annotation = self.annotate(fmt % value if lbl is None else lbl,
                                       xy, xytext, textcoords="offset points",
                                       ha=ha, va=va, **kwargs)
            annotations.append(annotation)

        return annotations
