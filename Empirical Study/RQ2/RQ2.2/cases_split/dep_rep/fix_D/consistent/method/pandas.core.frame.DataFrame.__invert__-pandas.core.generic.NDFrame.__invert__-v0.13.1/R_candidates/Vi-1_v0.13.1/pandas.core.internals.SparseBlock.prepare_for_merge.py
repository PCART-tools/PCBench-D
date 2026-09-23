    def prepare_for_merge(self, **kwargs):
        """ create a dense block """
        return make_block(self.get_values(), self.items, self.ref_items)
