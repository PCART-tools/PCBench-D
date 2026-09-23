    def on_changed(self, func):
        """
        When the slider value is changed call *func* with the new
        slider value

        Parameters
        ----------
        func : callable
            Function to call when slider is changed.
            The function must accept a single float as its arguments.

        Returns
        -------
        int
            Connection id (which can be used to disconnect *func*)
        """
        cid = self.cnt
        self.observers[cid] = func
        self.cnt += 1
        return cid
