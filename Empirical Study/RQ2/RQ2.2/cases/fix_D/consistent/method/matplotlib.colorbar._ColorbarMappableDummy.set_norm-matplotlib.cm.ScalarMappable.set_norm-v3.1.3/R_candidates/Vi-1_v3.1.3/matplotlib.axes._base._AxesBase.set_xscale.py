    def set_xscale(self, value, **kwargs):
        """
        Set the x-axis scale.

        Parameters
        ----------
        value : {"linear", "log", "symlog", "logit", ...}
            The axis scale type to apply.

        **kwargs
            Different keyword arguments are accepted, depending on the scale.
            See the respective class keyword arguments:

            - `matplotlib.scale.LinearScale`
            - `matplotlib.scale.LogScale`
            - `matplotlib.scale.SymmetricalLogScale`
            - `matplotlib.scale.LogitScale`


        Notes
        -----
        By default, Matplotlib supports the above mentioned scales.
        Additionally, custom scales may be registered using
        `matplotlib.scale.register_scale`. These scales can then also
        be used here.
        """
        g = self.get_shared_x_axes()
        for ax in g.get_siblings(self):
            ax.xaxis._set_scale(value, **kwargs)
            ax._update_transScale()
            ax.stale = True

        self.autoscale_view(scaley=False)
