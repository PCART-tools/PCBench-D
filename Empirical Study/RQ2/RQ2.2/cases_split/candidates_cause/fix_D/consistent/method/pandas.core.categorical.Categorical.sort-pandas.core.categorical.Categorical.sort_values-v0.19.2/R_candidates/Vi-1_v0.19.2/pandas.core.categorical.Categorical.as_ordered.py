    def as_ordered(self, inplace=False):
        """
        Sets the Categorical to be ordered

        Parameters
        ----------
        inplace : boolean (default: False)
           Whether or not to set the ordered attribute inplace or return a copy
           of this categorical with ordered set to True
        """
        return self.set_ordered(True, inplace=inplace)
