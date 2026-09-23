    def _changed(self):
        """
        Call this whenever the norm is changed to notify all the
        callback listeners to the 'changed' signal.
        """
        self.callbacks.process('changed')
