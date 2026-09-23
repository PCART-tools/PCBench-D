    def get(self, key, default=None):
        """
        Get item from object for given key (DataFrame column, Panel slice,
        etc.). Returns default value if not found.

        Parameters
        ----------
        key : object

        Returns
        -------
        value : same type as items contained in object
        """
        try:
            return self[key]
        except (KeyError, ValueError, IndexError):
            return default
