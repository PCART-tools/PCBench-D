    def set_adjustable(self, adjustable, share=False):
        """
        Define which parameter the Axes will change to achieve a given aspect.

        Parameters
        ----------
        adjustable : {'box', 'datalim'}
            If 'box', change the physical dimensions of the Axes.
            If 'datalim', change the ``x`` or ``y`` data limits.

        share : bool, optional
            If ``True``, apply the settings to all shared Axes.
            Default is ``False``.

        See Also
        --------
        matplotlib.axes.Axes.set_aspect
            for a description of aspect handling.

        Notes
        -----
        Shared Axes (of which twinned Axes are a special case)
        impose restrictions on how aspect ratios can be imposed.
        For twinned Axes, use 'datalim'.  For Axes that share both
        x and y, use 'box'.  Otherwise, either 'datalim' or 'box'
        may be used.  These limitations are partly a requirement
        to avoid over-specification, and partly a result of the
        particular implementation we are currently using, in
        which the adjustments for aspect ratios are done sequentially
        and independently on each Axes as it is drawn.
        """
        cbook._check_in_list(["box", "datalim"], adjustable=adjustable)
        if share:
            axs = {*self._shared_x_axes.get_siblings(self),
                   *self._shared_y_axes.get_siblings(self)}
        else:
            axs = [self]
        if (adjustable == "datalim"
                and any(getattr(ax.get_data_ratio, "__func__", None)
                        != _AxesBase.get_data_ratio
                        for ax in axs)):
            # Limits adjustment by apply_aspect assumes that the axes' aspect
            # ratio can be computed from the data limits and scales.
            raise ValueError("Cannot set axes adjustable to 'datalim' for "
                             "Axes which override 'get_data_ratio'")
        for ax in axs:
            ax._adjustable = adjustable
        self.stale = True
