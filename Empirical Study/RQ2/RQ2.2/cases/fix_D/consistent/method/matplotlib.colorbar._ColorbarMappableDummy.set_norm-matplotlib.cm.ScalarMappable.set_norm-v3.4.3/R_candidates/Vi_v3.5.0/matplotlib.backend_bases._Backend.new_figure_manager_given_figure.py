    @classmethod
    def new_figure_manager_given_figure(cls, num, figure):
        """Create a new figure manager instance for the given figure."""
        canvas = cls.FigureCanvas(figure)
        manager = cls.FigureManager(canvas, num)
        return manager
