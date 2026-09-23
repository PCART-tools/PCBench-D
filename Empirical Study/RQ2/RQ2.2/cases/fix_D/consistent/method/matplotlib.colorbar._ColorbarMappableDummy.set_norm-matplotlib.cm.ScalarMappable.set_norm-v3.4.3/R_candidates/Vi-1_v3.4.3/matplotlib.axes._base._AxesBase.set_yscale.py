    def set_yscale(self, value, **kwargs):
        """
        Set the y-axis scale.

        Parameters
        ----------
        value : {"linear", "log", "symlog", "logit", ...} or `.ScaleBase`
            The axis scale type to apply.

        **kwargs
            Different keyword arguments are accepted, depending on the scale.
            See the respective class keyword arguments:

            - `matplotlib.scale.LinearScale`
            - `matplotlib.scale.LogScale`
            - `matplotlib.scale.SymmetricalLogScale`
            - `matplotlib.scale.LogitScale`
            - `matplotlib.scale.FuncScale`

        Notes
        -----
        By default, Matplotlib supports the above mentioned scales.
        Additionally, custom scales may be registered using
        `matplotlib.scale.register_scale`. These scales can then also
        be used here.
        """
        old_default_lims = (self.yaxis.get_major_locator()
                            .nonsingular(-np.inf, np.inf))
        g = self.get_shared_y_axes()
        for ax in g.get_siblings(self):
            ax.yaxis._set_scale(value, **kwargs)
            ax._update_transScale()
            ax.stale = True
        new_default_lims = (self.yaxis.get_major_locator()
                            .nonsingular(-np.inf, np.inf))
        if old_default_lims != new_default_lims:
            # Force autoscaling now, to take advantage of the scale locator's
            # nonsingular() before it possibly gets swapped out by the user.
            self.autoscale_view(scalex=False)
