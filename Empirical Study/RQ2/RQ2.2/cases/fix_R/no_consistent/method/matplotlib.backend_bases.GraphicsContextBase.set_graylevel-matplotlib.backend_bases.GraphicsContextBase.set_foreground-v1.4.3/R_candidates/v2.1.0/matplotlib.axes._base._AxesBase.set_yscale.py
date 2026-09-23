    def set_yscale(self, value, **kwargs):
        """
        Set the y-axis scale

        Parameters
        ----------
        value : {"linear", "log", "symlog", "logit"}
            scaling strategy to apply

        Notes
        -----
        Different kwargs are accepted, depending on the scale. See
        the `~matplotlib.scale` module for more information.

        See also
        --------
        matplotlib.scale.LinearScale : linear transfrom

        matplotlib.scale.LogTransform : log transform

        matplotlib.scale.SymmetricalLogTransform : symlog transform

        matplotlib.scale.LogisticTransform : logit transform
        """
        # If the scale is being set to log, mask nonposy to prevent headaches
        # around zero
        if value.lower() == 'log' and 'nonposy' not in kwargs:
            kwargs['nonposy'] = 'mask'

        g = self.get_shared_y_axes()
        for ax in g.get_siblings(self):
            ax.yaxis._set_scale(value, **kwargs)
            ax._update_transScale()
            ax.stale = True
        self.autoscale_view(scalex=False)
