    def to_object_block(self, mgr):
        """ return myself as an object block """
        values = self.get_values(dtype=object)
        return self.make_block(values, klass=ObjectBlock)
