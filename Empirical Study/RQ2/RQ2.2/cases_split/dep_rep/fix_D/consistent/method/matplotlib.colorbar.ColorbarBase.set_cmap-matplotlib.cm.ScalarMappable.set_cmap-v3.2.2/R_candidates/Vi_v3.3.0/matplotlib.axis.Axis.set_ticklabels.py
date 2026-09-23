    def set_ticklabels(self, ticklabels, *, minor=False, **kwargs):
        r"""
        Set the text values of the tick labels.

        .. warning::
            This method should only be used after fixing the tick positions
            using `.Axis.set_ticks`. Otherwise, the labels may end up in
            unexpected positions.

        Parameters
        ----------
        ticklabels : sequence of str or of `.Text`\s
            Texts for labeling each tick location in the sequence set by
            `.Axis.set_ticks`; the number of labels must match the number of
            locations.
        minor : bool
            If True, set minor ticks instead of major ticks.
        **kwargs
            Text properties.

        Returns
        -------
        list of `.Text`\s
            For each tick, includes ``tick.label1`` if it is visible, then
            ``tick.label2`` if it is visible, in that order.
        """
        ticklabels = [t.get_text() if hasattr(t, 'get_text') else t
                      for t in ticklabels]
        locator = (self.get_minor_locator() if minor
                   else self.get_major_locator())
        if isinstance(locator, mticker.FixedLocator):
            # Passing [] as a list of ticklabels is often used as a way to
            # remove all tick labels, so only error for > 0 ticklabels
            if len(locator.locs) != len(ticklabels) and len(ticklabels) != 0:
                raise ValueError(
                    "The number of FixedLocator locations"
                    f" ({len(locator.locs)}), usually from a call to"
                    " set_ticks, does not match"
                    f" the number of ticklabels ({len(ticklabels)}).")
            tickd = {loc: lab for loc, lab in zip(locator.locs, ticklabels)}
            func = functools.partial(self._format_with_dict, tickd)
            formatter = mticker.FuncFormatter(func)
        else:
            formatter = mticker.FixedFormatter(ticklabels)

        if minor:
            self.set_minor_formatter(formatter)
            locs = self.get_minorticklocs()
            ticks = self.get_minor_ticks(len(locs))
        else:
            self.set_major_formatter(formatter)
            locs = self.get_majorticklocs()
            ticks = self.get_major_ticks(len(locs))

        ret = []
        for pos, (loc, tick) in enumerate(zip(locs, ticks)):
            tick.update_position(loc)
            tick_label = formatter(loc, pos)
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
