    def _scale_norm(self, norm, vmin, vmax):
        """
        Helper for initial scaling.

        Used by public functions that create a ScalarMappable and support
        parameters *vmin*, *vmax* and *norm*. This makes sure that a *norm*
        will take precedence over *vmin*, *vmax*.

        Note that this method does not set the norm.
        """
        if vmin is not None or vmax is not None:
            self.set_clim(vmin, vmax)
            if norm is not None:
                cbook.warn_deprecated(
                    "3.3",
                    message="Passing parameters norm and vmin/vmax "
                            "simultaneously is deprecated since %(since)s and "
                            "will become an error %(removal)s. Please pass "
                            "vmin/vmax directly to the norm when creating it.")

        # always resolve the autoscaling so we have concrete limits
        # rather than deferring to draw time.
        self.autoscale_None()
