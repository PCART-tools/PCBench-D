    def set(self, item, value):
        """
        Modify Block in-place with new item value

        Returns
        -------
        None
        """
        loc = self.items.get_loc(item)
        self.values[loc] = value
