    @property
    def is_bool(self):
        """ we can be a bool if we have only bool values but are of type
        object
        """
        return lib.is_bool_array(self.values.ravel())
