    def _delegate_property_set(self, name, new_values):
        return setattr(self.categorical, name, new_values)
