    def _to_safe_for_reshape(self):
        """ convert to object if we are a categorical """
        return self.astype('object')
