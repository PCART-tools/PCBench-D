    def _get_comb_axis(self, i):
        data_axis = self.objs[0]._get_block_manager_axis(i)
        try:
            return _get_objs_combined_axis(self.objs, axis=data_axis,
                                           intersect=self.intersect)
        except IndexError:
            types = [type(x).__name__ for x in self.objs]
            raise TypeError("Cannot concatenate list of {types}"
                            .format(types=types))
