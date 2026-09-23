    def _is_indexed_like(self, other):
        """
        Check all axes except items
        """
        if self.ndim != other.ndim:
            raise AssertionError(
                'Number of dimensions must agree got {ndim} and '
                '{oth_ndim}'.format(ndim=self.ndim, oth_ndim=other.ndim))
        for ax, oax in zip(self.axes[1:], other.axes[1:]):
            if not ax.equals(oax):
                return False
        return True
