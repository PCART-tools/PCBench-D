    def get_aux_axes(self, tr=None, viewlim_mode="equal", axes_class=Axes):
        """
        Add a parasite axes to this host.

        Despite this method's name, this should actually be thought of as an
        ``add_parasite_axes`` method.

        *tr* may be `.Transform`, in which case the following relation will
        hold: ``parasite.transData = tr + host.transData``.  Alternatively, it
        may be None (the default), no special relationship will hold between
        the parasite's and the host's ``transData``.
        """
        parasite_axes_class = parasite_axes_class_factory(axes_class)
        ax2 = parasite_axes_class(self, tr, viewlim_mode=viewlim_mode)
        # note that ax2.transData == tr + ax1.transData
        # Anything you draw in ax2 will match the ticks and grids of ax1.
        self.parasites.append(ax2)
        ax2._remove_method = self.parasites.remove
        return ax2
