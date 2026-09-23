    def as_unordered(self, inplace=False):
        """
        Sets the Categorical to be unordered

        Parameters
        ----------
        inplace : boolean (default: False)
           Whether or not to set the ordered attribute inplace or return a copy of this categorical
           with ordered set to False
        """
        return self.set_ordered(False, inplace=inplace)
