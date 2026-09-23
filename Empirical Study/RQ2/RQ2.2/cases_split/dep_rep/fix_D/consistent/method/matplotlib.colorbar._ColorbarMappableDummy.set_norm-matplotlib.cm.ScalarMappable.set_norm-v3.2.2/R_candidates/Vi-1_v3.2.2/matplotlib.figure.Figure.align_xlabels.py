    def align_xlabels(self, axs=None):
        """
        Align the ylabels of subplots in the same subplot column if label
        alignment is being done automatically (i.e. the label position is
        not manually set).

        Alignment persists for draw events after this is called.

        If a label is on the bottom, it is aligned with labels on axes that
        also have their label on the bottom and that have the same
        bottom-most subplot row.  If the label is on the top,
        it is aligned with labels on axes with the same top-most row.

        Parameters
        ----------
        axs : list of `~matplotlib.axes.Axes`
            Optional list of (or ndarray) `~matplotlib.axes.Axes`
            to align the xlabels.
            Default is to align all axes on the figure.

        See Also
        --------
        matplotlib.figure.Figure.align_ylabels

        matplotlib.figure.Figure.align_labels

        Notes
        -----
        This assumes that ``axs`` are from the same `.GridSpec`, so that
        their `.SubplotSpec` positions correspond to figure positions.

        Examples
        --------
        Example with rotated xtick labels::

            fig, axs = plt.subplots(1, 2)
            for tick in axs[0].get_xticklabels():
                tick.set_rotation(55)
            axs[0].set_xlabel('XLabel 0')
            axs[1].set_xlabel('XLabel 1')
            fig.align_xlabels()

        """

        if axs is None:
            axs = self.axes
        axs = np.asarray(axs).ravel()
        for ax in axs:
            _log.debug(' Working on: %s', ax.get_xlabel())
            ss = ax.get_subplotspec()
            nrows, ncols, row0, row1, col0, col1 = ss.get_rows_columns()
            labpo = ax.xaxis.get_label_position()  # top or bottom

            # loop through other axes, and search for label positions
            # that are same as this one, and that share the appropriate
            # row number.
            #  Add to a grouper associated with each axes of sibblings.
            # This list is inspected in `axis.draw` by
            # `axis._update_label_position`.
            for axc in axs:
                if axc.xaxis.get_label_position() == labpo:
                    ss = axc.get_subplotspec()
                    nrows, ncols, rowc0, rowc1, colc, col1 = \
                            ss.get_rows_columns()
                    if (labpo == 'bottom' and rowc1 == row1 or
                        labpo == 'top' and rowc0 == row0):
                        # grouper for groups of xlabels to align
                        self._align_xlabel_grp.join(ax, axc)
