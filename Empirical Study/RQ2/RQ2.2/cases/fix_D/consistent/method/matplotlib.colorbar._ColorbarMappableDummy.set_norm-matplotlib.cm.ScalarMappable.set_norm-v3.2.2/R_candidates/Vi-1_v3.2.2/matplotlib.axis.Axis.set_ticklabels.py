    def set_ticklabels(self, ticklabels, *args, minor=False, **kwargs):
        r"""
        Set the text values of the tick labels.

        Parameters
        ----------
        ticklabels : sequence of str or of `Text`\s
            List of texts for tick labels; must include values for non-visible
            labels.
        minor : bool
            If True, set minor ticks instead of major ticks.
        **kwargs
            Text properties.

        Returns
        -------
        labels : list of `Text`\s
            For each tick, includes ``tick.label1`` if it is visible, then
            ``tick.label2`` if it is visible, in that order.
        """
        if args:
            cbook.warn_deprecated(
                "3.1", message="Additional positional arguments to "
                "set_ticklabels are ignored, and deprecated since Matplotlib "
                "3.1; passing them will raise a TypeError in Matplotlib 3.3.")
        get_labels = []
        for t in ticklabels:
            # try calling get_text() to check whether it is Text object
            # if it is Text, get label content
            try:
                get_labels.append(t.get_text())
            # otherwise add the label to the list directly
            except AttributeError:
                get_labels.append(t)
        # replace the ticklabels list with the processed one
        ticklabels = get_labels

        if minor:
            self.set_minor_formatter(mticker.FixedFormatter(ticklabels))
            ticks = self.get_minor_ticks()
        else:
            self.set_major_formatter(mticker.FixedFormatter(ticklabels))
            ticks = self.get_major_ticks()
        ret = []
        for tick_label, tick in zip(ticklabels, ticks):
            # deal with label1
            tick.label1.set_text(tick_label)
            tick.label1.update(kwargs)
            # deal with label2
            tick.label2.set_text(tick_label)
            tick.label2.update(kwargs)
            # only return visible tick labels
            if tick.label1.get_visible():
                ret.append(tick.label1)
            if tick.label2.get_visible():
                ret.append(tick.label2)

        self.stale = True
        return ret
