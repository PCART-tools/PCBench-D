    def frozen(self):
        """
        Returns a frozen copy of this transform node.  The frozen copy
        will not update when its children change.  Useful for storing
        a previously known state of a transform where
        ``copy.deepcopy()`` might normally be used.
        """
        return self
