    def squeeze(self, axis=None):
        """
        Squeeze length 1 dimensions.

        Parameters
        ----------
        axis : None, integer or string axis name, optional
            The axis to squeeze if 1-sized.

            .. versionadded:: 0.20.0

        Returns
        -------
        scalar if 1-sized, else original object
        """
        axis = (self._AXIS_NAMES if axis is None else
                (self._get_axis_number(axis),))
        try:
            return self.iloc[
                tuple([0 if i in axis and len(a) == 1 else slice(None)
                       for i, a in enumerate(self.axes)])]
        except:
            return self
