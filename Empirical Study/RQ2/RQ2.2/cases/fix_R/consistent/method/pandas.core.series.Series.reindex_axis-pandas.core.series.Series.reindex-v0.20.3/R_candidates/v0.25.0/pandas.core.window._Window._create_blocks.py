    def _create_blocks(self):
        """
        Split data into blocks & return conformed data.
        """

        obj = self._selected_obj

        # filter out the on from the object
        if self.on is not None:
            if obj.ndim == 2:
                obj = obj.reindex(columns=obj.columns.difference([self.on]), copy=False)
        blocks = obj._to_dict_of_blocks(copy=False).values()

        return blocks, obj
