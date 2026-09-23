    def subplots(self, *, sharex=False, sharey=False, squeeze=True,
                 subplot_kw=None):
        """
        Add all subplots specified by this `GridSpec` to its parent figure.

        See `.Figure.subplots` for detailed documentation.
        """

        figure = self.figure

        if figure is None:
            raise ValueError("GridSpec.subplots() only works for GridSpecs "
                             "created with a parent figure")

        if isinstance(sharex, bool):
            sharex = "all" if sharex else "none"
        if isinstance(sharey, bool):
            sharey = "all" if sharey else "none"
        # This check was added because it is very easy to type
        # `subplots(1, 2, 1)` when `subplot(1, 2, 1)` was intended.
        # In most cases, no error will ever occur, but mysterious behavior
        # will result because what was intended to be the subplot index is
        # instead treated as a bool for sharex.  This check should go away
        # once sharex becomes kwonly.
        if isinstance(sharex, Integral):
            _api.warn_external(
                "sharex argument to subplots() was an integer.  Did you "
                "intend to use subplot() (without 's')?")
        _api.check_in_list(["all", "row", "col", "none"],
                           sharex=sharex, sharey=sharey)
        if subplot_kw is None:
            subplot_kw = {}
        # don't mutate kwargs passed by user...
        subplot_kw = subplot_kw.copy()

        # Create array to hold all axes.
        axarr = np.empty((self._nrows, self._ncols), dtype=object)
        for row in range(self._nrows):
            for col in range(self._ncols):
                shared_with = {"none": None, "all": axarr[0, 0],
                               "row": axarr[row, 0], "col": axarr[0, col]}
                subplot_kw["sharex"] = shared_with[sharex]
                subplot_kw["sharey"] = shared_with[sharey]
                axarr[row, col] = figure.add_subplot(
                    self[row, col], **subplot_kw)

        # turn off redundant tick labeling
        if sharex in ["col", "all"]:
            for ax in axarr[:-1, :].flat:  # Remove bottom labels/offsettexts.
                ax.xaxis.set_tick_params(which="both", labelbottom=False)
                if ax.xaxis.offsetText.get_position()[1] == 0:
                    ax.xaxis.offsetText.set_visible(False)
            for ax in axarr[1:, :].flat:  # Remove top labels/offsettexts.
                ax.xaxis.set_tick_params(which="both", labeltop=False)
                if ax.xaxis.offsetText.get_position()[1] == 1:
                    ax.xaxis.offsetText.set_visible(False)
        if sharey in ["row", "all"]:
            for ax in axarr[:, 1:].flat:  # Remove left labels/offsettexts.
                ax.yaxis.set_tick_params(which="both", labelleft=False)
                if ax.yaxis.offsetText.get_position()[0] == 0:
                    ax.yaxis.offsetText.set_visible(False)
            for ax in axarr[:, :-1].flat:  # Remove right labels/offsettexts.
                ax.yaxis.set_tick_params(which="both", labelright=False)
                if ax.yaxis.offsetText.get_position()[0] == 1:
                    ax.yaxis.offsetText.set_visible(False)

        if squeeze:
            # Discarding unneeded dimensions that equal 1.  If we only have one
            # subplot, just return it instead of a 1-element array.
            return axarr.item() if axarr.size == 1 else axarr.squeeze()
        else:
            # Returned axis array will be always 2-d, even if nrows=ncols=1.
            return axarr
