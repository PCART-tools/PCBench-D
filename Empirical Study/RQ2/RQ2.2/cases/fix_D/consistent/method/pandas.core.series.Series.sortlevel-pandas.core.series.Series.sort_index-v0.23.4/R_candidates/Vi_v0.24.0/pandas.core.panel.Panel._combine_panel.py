    def _combine_panel(self, other, func):
        items = self.items.union(other.items)
        major = self.major_axis.union(other.major_axis)
        minor = self.minor_axis.union(other.minor_axis)

        # could check that everything's the same size, but forget it
        this = self.reindex(items=items, major=major, minor=minor)
        other = other.reindex(items=items, major=major, minor=minor)

        with np.errstate(all='ignore'):
            result_values = func(this.values, other.values)

        return self._constructor(result_values, items, major, minor)
