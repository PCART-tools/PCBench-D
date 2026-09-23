    def _get_comb_axis(self, i: int) -> Index:
        data_axis = self.objs[0]._get_block_manager_axis(i)
        return get_objs_combined_axis(
            self.objs, axis=data_axis, intersect=self.intersect, sort=self.sort
        )
