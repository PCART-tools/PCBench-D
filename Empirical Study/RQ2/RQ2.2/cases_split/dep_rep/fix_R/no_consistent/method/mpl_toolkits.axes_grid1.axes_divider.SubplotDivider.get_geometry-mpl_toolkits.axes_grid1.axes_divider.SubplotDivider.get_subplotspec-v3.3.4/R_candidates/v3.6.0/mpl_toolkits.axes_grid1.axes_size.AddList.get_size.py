    def get_size(self, renderer):
        sum_rel_size = sum([a.get_size(renderer)[0] for a in self._list])
        sum_abs_size = sum([a.get_size(renderer)[1] for a in self._list])
        return sum_rel_size, sum_abs_size
