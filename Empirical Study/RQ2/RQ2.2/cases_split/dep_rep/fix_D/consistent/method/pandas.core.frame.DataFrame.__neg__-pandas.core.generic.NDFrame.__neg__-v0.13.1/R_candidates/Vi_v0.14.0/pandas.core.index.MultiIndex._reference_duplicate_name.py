    def _reference_duplicate_name(self, name):
        """
        Returns True if the name refered to in self.names is duplicated.
        """
        # count the times name equals an element in self.names.
        return np.sum(name == np.asarray(self.names)) > 1
