    def __init__(self, fig, *args, **kwargs):
        """
        Parameters
        ----------
        fig : `matplotlib.figure.Figure`

        *args : tuple (*nrows*, *ncols*, *index*) or int
            The array of subplots in the figure has dimensions ``(nrows,
            ncols)``, and *index* is the index of the subplot being created.
            *index* starts at 1 in the upper left corner and increases to the
            right.

            If *nrows*, *ncols*, and *index* are all single digit numbers, then
            *args* can be passed as a single 3-digit number (e.g. 234 for
            (2, 3, 4)).

        **kwargs
            Keyword arguments are passed to the Axes (sub)class constructor.
        """
        # _axes_class is set in the subplot_class_factory
        self._axes_class.__init__(self, fig, [0, 0, 1, 1], **kwargs)
        # This will also update the axes position.
        self.set_subplotspec(SubplotSpec._from_subplot_args(fig, args))
