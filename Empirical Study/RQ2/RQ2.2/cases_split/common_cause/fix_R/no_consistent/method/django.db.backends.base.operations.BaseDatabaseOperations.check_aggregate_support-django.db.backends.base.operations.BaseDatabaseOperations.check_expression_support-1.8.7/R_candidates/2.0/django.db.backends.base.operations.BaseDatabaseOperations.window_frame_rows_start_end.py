    def window_frame_rows_start_end(self, start=None, end=None):
        """
        Return SQL for start and end points in an OVER clause window frame.
        """
        if not self.connection.features.supports_over_clause:
            raise NotSupportedError('This backend does not support window expressions.')
        return self.window_frame_start(start), self.window_frame_end(end)
