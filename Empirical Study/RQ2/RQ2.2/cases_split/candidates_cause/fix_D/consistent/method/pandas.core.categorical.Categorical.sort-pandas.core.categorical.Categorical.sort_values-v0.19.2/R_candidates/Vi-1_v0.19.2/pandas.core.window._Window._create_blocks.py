    def _create_blocks(self, how):
        """ split data into blocks & return conformed data """

        obj, index = self._convert_freq(how)
        if index is not None:
            index = self._on

        # filter out the on from the object
        if self.on is not None:
            if obj.ndim == 2:
                obj = obj.reindex(columns=obj.columns.difference([self.on]),
                                  copy=False)
        blocks = obj.as_blocks(copy=False).values()

        return blocks, obj, index
