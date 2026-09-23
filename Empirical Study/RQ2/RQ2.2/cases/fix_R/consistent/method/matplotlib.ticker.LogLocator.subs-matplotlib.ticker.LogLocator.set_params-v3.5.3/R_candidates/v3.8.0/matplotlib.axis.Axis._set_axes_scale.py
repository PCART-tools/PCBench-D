    def _set_axes_scale(self, value, **kwargs):
        """
        Set this Axis' scale.

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
        By default, Matplotlib supports the above-mentioned scales.
        Additionally, custom scales may be registered using
        `matplotlib.scale.register_scale`. These scales can then also
        be used here.
        """
        name = self._get_axis_name()
        old_default_lims = (self.get_major_locator()
                            .nonsingular(-np.inf, np.inf))
        for ax in self._get_shared_axes():
            ax._axis_map[name]._set_scale(value, **kwargs)
            ax._update_transScale()
            ax.stale = True
        new_default_lims = (self.get_major_locator()
                            .nonsingular(-np.inf, np.inf))
        if old_default_lims != new_default_lims:
            # Force autoscaling now, to take advantage of the scale locator's
            # nonsingular() before it possibly gets swapped out by the user.
            self.axes.autoscale_view(
                **{f"scale{k}": k == name for k in self.axes._axis_names})
