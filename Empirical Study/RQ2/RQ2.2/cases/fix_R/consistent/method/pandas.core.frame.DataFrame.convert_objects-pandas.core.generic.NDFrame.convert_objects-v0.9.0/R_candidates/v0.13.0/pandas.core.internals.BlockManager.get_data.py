    def get_data(self, copy=False, columns=None, **kwargs):
        """
        Parameters
        ----------
        copy : boolean, default False
            Whether to copy the blocks
        """
        blocks = self.get_block_map(
            typ='list', copy=copy, columns=columns, **kwargs)
        if len(blocks) == 0:
            return self.make_empty()

        return self.combine(blocks)
