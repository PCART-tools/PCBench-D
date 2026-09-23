    def _set_name(self, name, inplace=False):
        """
        Set the Series name.

        Parameters
        ----------
        name : str
        inplace : bool
            whether to modify `self` directly or return a copy
        """
        ser = self if inplace else self.copy()
        ser.name = name
        return ser
