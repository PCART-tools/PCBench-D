    def _get_index(self, name):
        """ safe get index """
        try:
            return self.indices[name]
        except:
            if isinstance(name, Timestamp):
                name = name.value
                return self.indices[name]
            raise
