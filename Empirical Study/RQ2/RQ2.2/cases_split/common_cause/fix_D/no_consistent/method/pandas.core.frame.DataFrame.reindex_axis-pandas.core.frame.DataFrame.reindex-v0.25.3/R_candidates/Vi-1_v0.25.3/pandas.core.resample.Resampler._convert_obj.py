    def _convert_obj(self, obj):
        """
        Provide any conversions for the object in order to correctly handle.

        Parameters
        ----------
        obj : the object to be resampled

        Returns
        -------
        obj : converted object
        """
        obj = obj._consolidate()
        return obj
