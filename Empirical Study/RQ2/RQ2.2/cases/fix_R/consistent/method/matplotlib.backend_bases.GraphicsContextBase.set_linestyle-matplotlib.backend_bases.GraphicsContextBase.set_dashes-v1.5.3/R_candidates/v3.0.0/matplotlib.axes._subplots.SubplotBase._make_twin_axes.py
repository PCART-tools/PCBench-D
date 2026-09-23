    def _make_twin_axes(self, *kl, **kwargs):
        """
        Make a twinx axes of self. This is used for twinx and twiny.
        """
        from matplotlib.projections import process_projection_requirements
        if 'sharex' in kwargs and 'sharey' in kwargs:
            # The following line is added in v2.2 to avoid breaking Seaborn,
            # which currently uses this internal API.
            if kwargs["sharex"] is not self and kwargs["sharey"] is not self:
                raise ValueError("Twinned Axes may share only one axis.")
        kl = (self.get_subplotspec(),) + kl
        projection_class, kwargs, key = process_projection_requirements(
            self.figure, *kl, **kwargs)

        ax2 = subplot_class_factory(projection_class)(self.figure,
                                                      *kl, **kwargs)
        self.figure.add_subplot(ax2)
        self.set_adjustable('datalim')
        ax2.set_adjustable('datalim')

        if self._layoutbox is not None and ax2._layoutbox is not None:
            # make the layout boxes be explicitly the same
            ax2._layoutbox.constrain_same(self._layoutbox)
            ax2._poslayoutbox.constrain_same(self._poslayoutbox)

        self._twinned_axes.join(self, ax2)
        return ax2
