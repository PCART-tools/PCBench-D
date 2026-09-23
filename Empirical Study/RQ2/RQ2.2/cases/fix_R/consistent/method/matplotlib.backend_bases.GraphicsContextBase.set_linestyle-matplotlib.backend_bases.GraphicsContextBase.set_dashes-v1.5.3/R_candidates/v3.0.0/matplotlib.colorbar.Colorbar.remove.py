    def remove(self):
        """
        Remove this colorbar from the figure.  If the colorbar was created with
        ``use_gridspec=True`` then restore the gridspec to its previous value.
        """

        ColorbarBase.remove(self)
        self.mappable.callbacksSM.disconnect(self.mappable.colorbar_cid)
        self.mappable.colorbar = None
        self.mappable.colorbar_cid = None

        try:
            ax = self.mappable.axes
        except AttributeError:
            return

        try:
            gs = ax.get_subplotspec().get_gridspec()
            subplotspec = gs.get_topmost_subplotspec()
        except AttributeError:
            # use_gridspec was False
            pos = ax.get_position(original=True)
            ax._set_position(pos)
        else:
            # use_gridspec was True
            ax.set_subplotspec(subplotspec)
