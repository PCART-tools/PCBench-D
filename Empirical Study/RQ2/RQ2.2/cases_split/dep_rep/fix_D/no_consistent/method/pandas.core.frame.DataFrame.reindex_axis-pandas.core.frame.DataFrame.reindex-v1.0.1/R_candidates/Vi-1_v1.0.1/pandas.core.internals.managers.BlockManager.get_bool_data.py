    def get_bool_data(self, copy=False):
        """
        Parameters
        ----------
        copy : boolean, default False
            Whether to copy the blocks
        """
        self._consolidate_inplace()
        return self.combine([b for b in self.blocks if b.is_bool], copy)
