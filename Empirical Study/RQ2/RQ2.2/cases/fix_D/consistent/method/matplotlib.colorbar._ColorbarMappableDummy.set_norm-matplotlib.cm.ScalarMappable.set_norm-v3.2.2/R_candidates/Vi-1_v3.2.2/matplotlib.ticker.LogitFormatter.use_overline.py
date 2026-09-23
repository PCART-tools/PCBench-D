    def use_overline(self, use_overline):
        r"""
        Switch display mode with overline for labelling p>1/2.

        Parameters
        ----------
        use_overline : bool, default: False
            If x > 1/2, with x = 1-v, indicate if x should be displayed as
            $\overline{v}$. The default is to display $1-v$.
        """
        self._use_overline = use_overline
