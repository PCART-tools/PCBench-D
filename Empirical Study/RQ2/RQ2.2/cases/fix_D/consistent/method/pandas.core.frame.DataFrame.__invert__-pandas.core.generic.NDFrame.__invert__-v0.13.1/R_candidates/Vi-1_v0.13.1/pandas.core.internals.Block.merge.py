    def merge(self, other):
        if not self.ref_items.equals(other.ref_items):
            raise AssertionError('Merge operands must have same ref_items')

        # Not sure whether to allow this or not
        # if not union_ref.equals(other.ref_items):
        #     union_ref = self.ref_items + other.ref_items
        return _merge_blocks([self, other], self.ref_items)
