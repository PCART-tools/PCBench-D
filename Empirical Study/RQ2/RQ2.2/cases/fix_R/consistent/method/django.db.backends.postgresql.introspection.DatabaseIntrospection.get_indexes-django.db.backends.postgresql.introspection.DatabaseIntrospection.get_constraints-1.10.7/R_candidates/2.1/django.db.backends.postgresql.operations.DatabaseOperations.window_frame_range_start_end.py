    def window_frame_range_start_end(self, start=None, end=None):
        start_, end_ = super().window_frame_range_start_end(start, end)
        if (start and start < 0) or (end and end > 0):
            raise NotSupportedError(
                'PostgreSQL only supports UNBOUNDED together with PRECEDING '
                'and FOLLOWING.'
            )
        return start_, end_
