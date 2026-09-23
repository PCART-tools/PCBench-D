    def align_ylabels(self, axs=None):
        """
        Align the ylabels of subplots in the same subplot column if label
        alignment is being done automatically (i.e. the label position is
        not manually set).

        Alignment persists for draw events after this is called.

        If a label is on the left, it is aligned with labels on axes that
        also have their label on the left and that have the same
        left-most subplot column.  If the label is on the right,
        it is aligned with labels on axes with the same right-most column.

        Parameters
        ----------
        axs : list of `~matplotlib.axes.Axes`
            Optional list (or ndarray) of `~matplotlib.axes.Axes`
            to align the ylabels.
            Default is to align all axes on the figure.

        See Also
        --------
        matplotlib.figure.Figure.align_xlabels

        matplotlib.figure.Figure.align_labels

        Notes
        -----
        This assumes that ``axs`` are from the same `.GridSpec`, so that
        their `.SubplotSpec` positions correspond to figure positions.

        Examples
        --------
        Example with large yticks labels::

            fig, axs = plt.subplots(2, 1)
            axs[0].plot(np.arange(0, 1000, 50))
            axs[0].set_ylabel('YLabel 0')
            axs[1].set_ylabel('YLabel 1')
            fig.align_ylabels()

        """

        if axs is None:
            axs = self.axes
        axs = np.asarray(axs).ravel()
        for ax in axs:
            _log.debug(' Working on: %s', ax.get_ylabel())
            ss = ax.get_subplotspec()
            nrows, ncols, row0, row1, col0, col1 = ss.get_rows_columns()
            same = [ax]
            labpo = ax.yaxis.get_label_position()  # left or right
            # loop through other axes, and search for label positions
            # that are same as this one, and that share the appropriate
            # column number.
            # Add to a list associated with each axes of sibblings.
            # This list is inspected in `axis.draw` by
            # `axis._update_label_position`.
            for axc in axs:
                if axc != ax:
                    if axc.yaxis.get_label_position() == labpo:
                        ss = axc.get_subplotspec()
                        nrows, ncols, row0, row1, colc0, colc1 = \
                                ss.get_rows_columns()
                        if (labpo == 'left' and colc0 == col0 or
                            labpo == 'right' and colc1 == col1):
                            # grouper for groups of ylabels to align
                            self._align_ylabel_grp.join(ax, axc)
