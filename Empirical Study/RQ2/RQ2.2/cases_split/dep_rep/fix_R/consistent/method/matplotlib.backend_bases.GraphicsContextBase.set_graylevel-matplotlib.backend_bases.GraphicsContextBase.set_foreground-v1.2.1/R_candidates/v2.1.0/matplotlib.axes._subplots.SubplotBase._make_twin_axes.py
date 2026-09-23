    def _make_twin_axes(self, *kl, **kwargs):
        """
        make a twinx axes of self. This is used for twinx and twiny.
        """
        from matplotlib.projections import process_projection_requirements
        kl = (self.get_subplotspec(),) + kl
        projection_class, kwargs, key = process_projection_requirements(
            self.figure, *kl, **kwargs)

        ax2 = subplot_class_factory(projection_class)(self.figure,
                                                      *kl, **kwargs)
        self.figure.add_subplot(ax2)
        return ax2
