    def get_new_index(self):
        result_labels = []
        for cur in self.sorted_labels[:-1]:
            labels = cur.take(self.compressor)
            labels = _make_index_array_level(labels, cur)
            result_labels.append(labels)

        # construct the new index
        if len(self.new_index_levels) == 1:
            new_index = self.new_index_levels[0]
            new_index.name = self.new_index_names[0]
        else:
            new_index = MultiIndex(levels=self.new_index_levels,
                                   labels=result_labels,
                                   names=self.new_index_names,
                                   verify_integrity=False)

        return new_index
