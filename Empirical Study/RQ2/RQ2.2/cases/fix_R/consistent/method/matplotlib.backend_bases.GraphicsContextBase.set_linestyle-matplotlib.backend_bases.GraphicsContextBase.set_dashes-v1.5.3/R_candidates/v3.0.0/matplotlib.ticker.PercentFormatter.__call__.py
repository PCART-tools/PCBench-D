    def __call__(self, x, pos=None):
        """
        Formats the tick as a percentage with the appropriate scaling.
        """
        ax_min, ax_max = self.axis.get_view_interval()
        display_range = abs(ax_max - ax_min)

        return self.fix_minus(self.format_pct(x, display_range))
