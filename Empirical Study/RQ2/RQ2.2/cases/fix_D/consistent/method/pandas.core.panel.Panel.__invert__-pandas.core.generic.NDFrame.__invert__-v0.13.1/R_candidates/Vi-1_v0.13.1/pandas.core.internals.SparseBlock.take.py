    def take(self, indexer, ref_items, new_axis, axis=1):
        """ going to take our items
            along the long dimension"""
        if axis < 1:
            raise AssertionError('axis must be at least 1, got %d' % axis)

        return [self.make_block(self.values.take(indexer))]
