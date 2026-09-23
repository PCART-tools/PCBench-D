    def _set_result_index_ordered(self, result):
        # set the result index on the passed values object
        # return the new object
        # related 8046

        # the values/counts are repeated according to the group index
        indices = self.indices

        # shortcut of we have an already ordered grouper
        if not self.grouper.is_monotonic:
            index = Index(np.concatenate([ indices[v] for v in self.grouper.result_index ]))
            result.index = index
            result = result.sort_index()

        result.index = self.obj.index
        return result
