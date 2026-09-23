    def _get_attributes_dict(self):
        """ return an attributes dict for my class """
        return dict([(k, getattr(self, k, None)) for k in self._attributes])
