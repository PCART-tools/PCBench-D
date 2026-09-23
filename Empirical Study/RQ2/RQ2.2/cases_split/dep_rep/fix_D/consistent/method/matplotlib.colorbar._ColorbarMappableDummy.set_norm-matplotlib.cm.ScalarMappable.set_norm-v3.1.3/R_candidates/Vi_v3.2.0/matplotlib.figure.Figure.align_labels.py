    def align_labels(self, axs=None):
        """
        Align the xlabels and ylabels of subplots with the same subplots
        row or column (respectively) if label alignment is being
        done automatically (i.e. the label position is not manually set).

        Alignment persists for draw events after this is called.

        Parameters
        ----------
        axs : list of `~matplotlib.axes.Axes`
            Optional list (or ndarray) of `~matplotlib.axes.Axes`
            to align the labels.
            Default is to align all axes on the figure.

        See Also
        --------
        matplotlib.figure.Figure.align_xlabels

        matplotlib.figure.Figure.align_ylabels
        """
        self.align_xlabels(axs=axs)
        self.align_ylabels(axs=axs)
