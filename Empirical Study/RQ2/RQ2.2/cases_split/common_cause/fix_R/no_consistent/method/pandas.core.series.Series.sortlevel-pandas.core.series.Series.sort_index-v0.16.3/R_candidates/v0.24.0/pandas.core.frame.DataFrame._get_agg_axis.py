    def _get_agg_axis(self, axis_num):
        """
        Let's be explicit about this.
        """
        if axis_num == 0:
            return self.columns
        elif axis_num == 1:
            return self.index
        else:
            raise ValueError('Axis must be 0 or 1 (got %r)' % axis_num)
