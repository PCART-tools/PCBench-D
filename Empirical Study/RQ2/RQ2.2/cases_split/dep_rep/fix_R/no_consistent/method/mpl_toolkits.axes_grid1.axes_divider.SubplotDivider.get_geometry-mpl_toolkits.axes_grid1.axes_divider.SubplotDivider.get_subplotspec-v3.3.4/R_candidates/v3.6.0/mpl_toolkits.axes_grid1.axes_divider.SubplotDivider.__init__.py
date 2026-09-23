    def __init__(self, fig, *args, horizontal=None, vertical=None,
                 aspect=None, anchor='C'):
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
        """
        self.figure = fig
        super().__init__(fig, [0, 0, 1, 1],
                         horizontal=horizontal or [], vertical=vertical or [],
                         aspect=aspect, anchor=anchor)
        self.set_subplotspec(SubplotSpec._from_subplot_args(fig, args))
