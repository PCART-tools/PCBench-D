    def set_ticklabels(self, ticklabels, *args, **kwargs):
        """
        Set the text values of the tick labels. Return a list of Text
        instances.  Use *kwarg* *minor=True* to select minor ticks.
        All other kwargs are used to update the text object properties.
        As for get_ticklabels, label1 (left or bottom) is
        affected for a given tick only if its label1On attribute
        is True, and similarly for label2.  The list of returned
        label text objects consists of all such label1 objects followed
        by all such label2 objects.

        The input *ticklabels* is assumed to match the set of
        tick locations, regardless of the state of label1On and
        label2On.

        ACCEPTS: sequence of strings or Text objects
        """
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

        minor = kwargs.pop('minor', False)
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
            if tick.label1On:
                ret.append(tick.label1)
            if tick.label2On:
                ret.append(tick.label2)

        self.stale = True
        return ret
