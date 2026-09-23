    def window_frame_end(self, end):
        if isinstance(end, int):
            if end == 0:
                return self.CURRENT_ROW
            elif end > 0:
                return '%d %s' % (end, self.FOLLOWING)
        elif end is None:
            return self.UNBOUNDED_FOLLOWING
        raise ValueError("end argument must be a positive integer, zero, or None, but got '%s'." % end)
