    def finish(self):
        # Call run here now that all frame grabbing is done. All temp files
        # are available to be assembled.
        self._run()
        super().finish()  # Will call clean-up
