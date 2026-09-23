    def _to_safe_for_reshape(self):
        """ convert to object if we are a categorical """
        return self.set_levels([i._to_safe_for_reshape() for i in self.levels])
