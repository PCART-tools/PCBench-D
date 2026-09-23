    def to_tuples(self):
        return Index(com._asarray_tuplesafe(zip(self.left, self.right)))
