    def _make_twin_axes(self, *args, **kwargs):
        """Make a twinx axes of self. This is used for twinx and twiny."""
        if 'sharex' in kwargs and 'sharey' in kwargs:
            # The following line is added in v2.2 to avoid breaking Seaborn,
            # which currently uses this internal API.
            if kwargs["sharex"] is not self and kwargs["sharey"] is not self:
                raise ValueError("Twinned Axes may share only one axis")
        # The dance here with label is to force add_subplot() to create a new
        # Axes (by passing in a label never seen before).  Note that this does
        # not affect plot reactivation by subplot() as twin axes can never be
        # reactivated by subplot().
        sentinel = str(uuid.uuid4())
        real_label = kwargs.pop("label", sentinel)
        twin = self.figure.add_subplot(
            self.get_subplotspec(), *args, label=sentinel, **kwargs)
        if real_label is not sentinel:
            twin.set_label(real_label)
        self.set_adjustable('datalim')
        twin.set_adjustable('datalim')
        if self._layoutbox is not None and twin._layoutbox is not None:
            # make the layout boxes be explicitly the same
            twin._layoutbox.constrain_same(self._layoutbox)
            twin._poslayoutbox.constrain_same(self._poslayoutbox)
        self._twinned_axes.join(self, twin)
        return twin
