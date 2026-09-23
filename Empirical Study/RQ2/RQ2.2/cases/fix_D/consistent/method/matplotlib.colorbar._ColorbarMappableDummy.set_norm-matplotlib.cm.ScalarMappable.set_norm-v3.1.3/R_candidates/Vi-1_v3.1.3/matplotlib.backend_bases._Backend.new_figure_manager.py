    @classmethod
    def new_figure_manager(cls, num, *args, **kwargs):
        """Create a new figure manager instance.
        """
        # This import needs to happen here due to circular imports.
        from matplotlib.figure import Figure
        fig_cls = kwargs.pop('FigureClass', Figure)
        fig = fig_cls(*args, **kwargs)
        return cls.new_figure_manager_given_figure(num, fig)
